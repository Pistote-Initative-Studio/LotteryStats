# LotteryStats

LotteryStats provides the data backbone for tracking U.S. lottery draw history and derived statistics. This repository currently ships the production-ready database schema and operational docs to stand up the first environment.

## What's in this repo?

- `migrations/V1__init.sql` – idempotent Postgres migration defining the canonical schema and seed data.
- `docs/cron_schedule.md` – high-level schedule for recurring jobs.
- `docs/runbook.md` – operational outline for the ingest → normalize → upsert → rollup pipeline.
- `.editorconfig`, `.gitignore`, `.env.example` – project hygiene and configuration templates.

## Running the migration on Neon

1. Create a new Postgres database in Neon and copy the connection string for reference.
2. Open the **SQL Editor** in the Neon dashboard.
3. Paste the contents of `migrations/V1__init.sql` into the editor and execute it. The migration is idempotent, so re-running it is safe.
4. (Optional) Connect via psql using your Neon connection string to automate migrations later.

## Quick verification queries

Run these queries in Neon to confirm the schema:

```sql
-- Confirm migration bookkeeping and seed lotteries
SELECT version, applied_at FROM migrations ORDER BY applied_at DESC;
SELECT lottery_code, lottery_name, timezone FROM lotteries ORDER BY lottery_code;

-- Inspect the most recent normalized draws and rollups
SELECT lottery_code, draw_identifier, draw_date FROM normalized_draws ORDER BY draw_date DESC LIMIT 5;
SELECT lottery_code, metric_name, rollup_window, bucket_start, metric_value FROM stats_rollup ORDER BY bucket_start DESC LIMIT 5;
```

If the tables return zero rows (expected on a fresh database) but execute without errors, the migration has been applied successfully.

## Next steps

Future work will add application services to load raw draw data, normalize results, and maintain rollups on a schedule aligned with the included cron and runbook documentation.
