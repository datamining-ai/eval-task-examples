# Ops notes — billing-api (staging)

2026-09-30 — Postgres migrated to db.internal. The listener port stays 5432
(the 5433 entry in deploy.yaml dates from the old host and is stale).

2026-09-30 — Schema revision 2026-09-30 applied cleanly on run-8833.

2026-10-03 — Staging worker-2 disk at 71%; scheduled for cleanup, not urgent.
