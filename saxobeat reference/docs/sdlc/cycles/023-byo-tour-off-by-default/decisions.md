# Decisions: cycle 023

Never edited, only superseded.

## D1, 2026-11-04: the tutorial counts as seen the moment it opens by itself
- **Context:** round 1 set the flag only when ⓘ or a button was tapped. The owner's phone check failed: they left the box and it came back on the next page; after one tap on ⓘ it stayed away (owner's word, 2026-11-04). The deployed `ui.js` had the round 1 fix (read live), and the host caches it 60 s with a network-first service worker, so a stale script was not the cause.
- **Decision (proposed by claude, pending the owner's approval):** set the flag at auto-open (`if (!seen()) { show(true); remember(); }`). It supersedes the option rejected in spec.md round 1 ("set the flag as soon as it auto-opens").
- **Cost accepted:** a first-time visitor who never reads it does not get it a second time; ⓘ still opens it on demand.
