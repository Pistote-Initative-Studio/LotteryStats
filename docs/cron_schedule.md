# Daily Cron Schedule

- **Job:** lottery stats rollup pipeline
- **When:** Every day at 5:00 AM Eastern Time (schedule string: `0 5 * * *` in `America/New_York`)
- **Why:** Ensures overnight draws are ingested, normalized, and aggregated before business hours.
- **Notes:** Run from an environment with the project `.env` configuration so database credentials resolve correctly.
