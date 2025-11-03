# LotteryStats Operations Runbook

1. **Ingest**
   - Pull raw draw payloads from upstream APIs or file drops.
   - Store the unmodified response in `draw_ingest_queue` with the source identifier and timestamp.
2. **Normalize**
   - Parse the payload, harmonize number formats, and calculate derived fields such as jackpots and sales.
   - Upsert standardized records into `normalized_draws` keyed by `(lottery_code, draw_identifier)`.
3. **Upsert & Audit**
   - Log operational events (success, retries, anomalies) into `audit_events` for traceability.
   - Ensure failed batches are retried before the next scheduled window.
4. **Rollups**
   - Aggregate normalized draws into `stats_rollup`, grouped by metric (`metric_name`) and `rollup_window`.
   - Maintain descending indexes to optimize dashboards querying the most recent `bucket_start` values.
5. **Verification**
   - Check `migrations` for the latest version string and monitor `audit_events` for recent entries.
   - Sample recent rows in `normalized_draws` and `stats_rollup` to confirm successful processing.
