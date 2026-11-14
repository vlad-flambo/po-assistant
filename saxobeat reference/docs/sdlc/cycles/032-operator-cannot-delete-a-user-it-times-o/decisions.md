# Decisions: cycle 032

## 2026-11-06: the list of tables grew by two (PageFetch, FetchAttempt)
The spec's design listed the tables that hang off a candidate, and `JobSource` for private jobs. The guard test (criterion 4), walking Django's relation graph from `Job`, also found `PageFetch` and `FetchAttempt`, which hang off a job (the Welcome to the Jungle page reader). They are deleted with the private jobs like `JobSource`. Nothing else in the design changed; this is what the guard was for.

## 2026-11-06: the person's own deletion deletes first, signs out after
`/account/delete/` used to sign the person out and then delete. If the delete failed they were signed out with the account still there and no message. Now it deletes first; on failure they stay signed in and see "nothing was deleted"; on success it signs them out as before. (Signing out only matters for an operator viewing as someone: `_end_viewing`; a person has nothing to end.)

## 2026-11-06: French text for the new person-facing error (done)
The new message ("Something went wrong and nothing was deleted...") is wrapped for translation, but this PC has no `msgfmt`, so `django.po`/`django.mo` were not touched (both also carry other cycles' uncommitted work). Until compiled, French users would see it in English. Deferred to Learn.
Resolved the same day: the repo's own `manage.py i18n extract`, the French text added by hand in `django.po`, `manage.py i18n compile` (babel, no `msgfmt` needed). The extract changed only my string and the creation date line. The `.po`/`.mo` still also carry other cycles' uncommitted work, so commit them together with care.

## 2026-11-06: a 30 s statement timeout on Postgres
One drill run on Postgres sat 9 minutes on a single DELETE and could not be reproduced (`evidence/after-postgres-2026-11-06.md`). The delete now sets `statement_timeout = 30s` for its transaction on Postgres only. A healthy statement takes well under a second; a bad plan fails, rolls back and the operator gets the error message. It bounds the damage, it does not explain the cause.
