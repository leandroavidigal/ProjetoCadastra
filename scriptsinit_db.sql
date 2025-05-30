CREATE TABLE assets (
  id           TEXT PRIMARY KEY,
  name         TEXT NOT NULL,
  symbol       TEXT NOT NULL,
  rank         INTEGER,
  priceUsd     DOUBLE PRECISION,
  marketCapUsd DOUBLE PRECISION
);

CREATE TABLE asset_history (
  id           SERIAL PRIMARY KEY,
  asset_id     TEXT NOT NULL REFERENCES assets(id),
  time         TIMESTAMP NOT NULL,
  priceUsd     DOUBLE PRECISION,
  volumeUsd24h DOUBLE PRECISION,
  marketCapUsd DOUBLE PRECISION,
  UNIQUE (asset_id, time)
);
