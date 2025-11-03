BEGIN;

CREATE TABLE IF NOT EXISTS migrations (
    version TEXT PRIMARY KEY,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS lotteries (
    lottery_code TEXT PRIMARY KEY,
    lottery_name TEXT NOT NULL,
    timezone TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS draw_ingest_queue (
    id BIGSERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    lottery_code TEXT NOT NULL,
    draw_identifier TEXT NOT NULL,
    draw_date TIMESTAMPTZ NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (lottery_code, draw_identifier)
);

CREATE INDEX IF NOT EXISTS draw_ingest_queue_recent_idx
    ON draw_ingest_queue (lottery_code, draw_date DESC);

CREATE TABLE IF NOT EXISTS normalized_draws (
    lottery_code TEXT NOT NULL,
    draw_identifier TEXT NOT NULL,
    draw_date DATE NOT NULL,
    jackpot NUMERIC(20,2),
    sales NUMERIC(20,2),
    winning_numbers SMALLINT[] NOT NULL,
    bonus_numbers SMALLINT[],
    normalized_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source_name TEXT NOT NULL,
    PRIMARY KEY (lottery_code, draw_identifier)
);

CREATE INDEX IF NOT EXISTS normalized_draws_recent_idx
    ON normalized_draws (lottery_code, draw_date DESC, normalized_at DESC);

CREATE TABLE IF NOT EXISTS stats_rollup (
    lottery_code TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    rollup_window TEXT NOT NULL,
    bucket_start DATE NOT NULL,
    bucket_end DATE NOT NULL,
    metric_value NUMERIC(20,2) NOT NULL,
    sample_size BIGINT,
    computed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB,
    PRIMARY KEY (lottery_code, metric_name, rollup_window, bucket_start)
);

CREATE INDEX IF NOT EXISTS stats_rollup_recent_idx
    ON stats_rollup (lottery_code, metric_name, rollup_window, bucket_start DESC);

CREATE TABLE IF NOT EXISTS audit_events (
    id BIGSERIAL PRIMARY KEY,
    event_type TEXT NOT NULL,
    event_context JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS audit_events_recent_idx
    ON audit_events (event_type, created_at DESC);

INSERT INTO lotteries (lottery_code, lottery_name, timezone)
VALUES
    ('powerball', 'Powerball', 'America/New_York'),
    ('mega_millions', 'Mega Millions', 'America/New_York'),
    ('lotto_america', 'Lotto America', 'America/Chicago')
ON CONFLICT (lottery_code) DO UPDATE
SET lottery_name = EXCLUDED.lottery_name,
    timezone = EXCLUDED.timezone,
    updated_at = NOW();

INSERT INTO migrations (version, applied_at)
VALUES ('V1__init', NOW())
ON CONFLICT (version) DO UPDATE
SET applied_at = EXCLUDED.applied_at;

COMMIT;
