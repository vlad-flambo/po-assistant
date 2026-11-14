"""Cycle 021, slices 2 and 3: write the two files the owner and the spec need from the glossary.

    DATABASE_URL=postgres://...replay021 uv run python docs/sdlc/cycles/021-bilingual-keyword-scoring/evidence/glossary_report.py

- keyword_coverage.md: for each keyword of the candidates C-01 and C-03 (read from the scratch copy of the dump), its concept or "none" with the reason;
- title_words_coverage.md: the 200 most frequent title words of each language in the dump, and whether a concept uses them;
- glossary_for_review.md: the whole glossary, one concept per line, English and French side by side (for the owner's reading, slice 3).

Read only. Reasons for the keywords without a concept are in REASONS below (written by hand).
"""

from __future__ import annotations

import collections
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
sys.path.insert(0, str(ROOT))

import django

django.setup()

from jobs import glossary
from jobs.models import Config, Job
from jobs.services.similarity import STOPWORDS
from jobs.text import normalize

REASONS = {
    "hybrid": "",  # covered
    "international": "the same word in both languages: nothing to add",
    "fintech": "the same word in both languages",
    "leadership": "the same word in both languages",
    "implementation": "French 'implémentation' is the same word once accents are dropped; the usual French phrase ('mise en œuvre') is in most job texts and would add noise",
    "chief of staff": "used as it is in French job texts; no standard French equivalent",
    "product builder": "a niche English title, no standard French equivalent",
    "global team": "",
    "llm": "",
    "hypergrowth": "",
    "client-facing": "",
}


def keyword_coverage(out: list[str]) -> None:
    for pk, label in ((1, "C-01 vlad"), (3, "C-03 Proto Type (a test profile with leftovers of a CV import as keywords)")):
        cfg = Config.objects.get(candidate_id=pk)
        include = cfg.keywords.get("include") or {}
        covered, none = [], []
        for kw, weight in include.items():
            c = glossary.concept_of(kw)
            (covered if c else none).append((kw, weight, c))
        out.append(f"\n## {label}: {len(include)} include keywords, {len(covered)} with a concept, {len(none)} without\n")
        if pk == 1:
            out.append("| Keyword | Weight | Concept (English = French) |\n|---|---|---|")
            for kw, weight, c in sorted(covered, key=lambda x: -x[1]):
                out.append(f"| {kw} | {weight:g} | {' ; '.join(c.en)} = {' ; '.join(c.fr)} |")
            out.append("\n| Keyword without a concept | Weight | Why |\n|---|---|---|")
            for kw, weight, _ in sorted(none, key=lambda x: -x[1]):
                out.append(f"| {kw} | {weight:g} | {REASONS.get(kw.lower(), 'no standard equivalent found; to add if the owner knows one')} |")
        else:
            out.append("Numbers, file formats, school and tool names from a developer's CV (`01`, `CSS`, `SQL`, `HTML`, `ISTY`...): the same in both languages or not job-search words, so none has an equivalent to add. "
                       f"Of the {len(include)}, the ones with a concept: {', '.join(k for k, _, _ in covered) or 'none'}.")


def title_words_coverage(out: list[str]) -> None:
    used = {w for c in glossary.CONCEPTS for t in c.terms for w in t.split()}
    for lang in ("fr", "en"):
        counter: collections.Counter = collections.Counter()
        for title in Job.objects.filter(language=lang).values_list("title", flat=True):
            counter.update({w for w in normalize(title).split() if w not in STOPWORDS and len(w) > 2 and not w.isdigit()})
        top = counter.most_common(200)
        inside = [(w, n) for w, n in top if w in used]
        outside = [(w, n) for w, n in top if w not in used]
        out.append(f"\n## {lang.upper()}: of the 200 most frequent title words, {len(inside)} are used in a concept, {len(outside)} are not\n")
        out.append("Not used (the same word in both languages, a place, a contract, a level, a sector of no interest to the owner, or no safe equivalent): "
                   + ", ".join(f"{w} ({n})" for w, n in outside))


def review(out: list[str]) -> None:
    out.append(f"# The bilingual glossary, for the owner's reading ({len(glossary.CONCEPTS)} concepts)\n")
    out.append("Read each line: the English terms on the left mean the same, for a job search, as the French ones on the right. "
               "Tell me which lines to change or remove. **[role]** marks a title or function. A term marked ⊘fr or ⊘en is not searched as an equivalent in postings of that language "
               "(for example 'ai' in French postings: it is the verb 'j'ai'). Accents are dropped on purpose: the scoring ignores them.\n")
    out.append("**False friends kept out of every concept** (they look alike and mean something else): " + ", ".join(sorted(glossary.FALSE_FRIENDS)) + ".\n")
    out.append("| # | English | French | |\n|---|---|---|---|")
    for c in glossary.CONCEPTS:
        def show(terms):
            return " ; ".join(t + "".join(f" ⊘{lang}" for lang in sorted(c.skip.get(t, ()))) for t in terms)
        out.append(f"| {c.key} | {show(c.en)} | {show(c.fr)} | {'role' if c.role else ''} |")
    out.append("\n- [ ] Owner read the list (corrections applied, tests re-run)")


def main() -> int:
    for name, fn, title in (("keyword_coverage.md", keyword_coverage, "# Which keywords the glossary covers (slice 2, criterion 2)\n\nSource: the keyword lists in the 29 Oct dump (scratch copy)."),
                            ("title_words_coverage.md", title_words_coverage, "# The most frequent title words and the glossary (slice 2, criterion 2)\n\nSource: the titles of the postings in the 29 Oct dump, by `Job.language`.")):
        out = [title]
        fn(out)
        (HERE / name).write_text("\n".join(out) + "\n", encoding="utf-8")
        print("wrote", name)
    out: list[str] = []
    review(out)
    (HERE / "glossary_for_review.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("wrote glossary_for_review.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
