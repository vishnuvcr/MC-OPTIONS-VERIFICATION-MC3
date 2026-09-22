# Historical index-price cache

The prospective engine keeps daily index closes locally after first retrieval and reuses them on subsequent runs.

Files are created/updated by the market adapter and carry a companion metadata file with retrieval timestamp and source URL.

- NIFTY: ^NSEI
- SENSEX: ^BSESN

The cache is research data, not an exchange-authoritative settlement feed. It is used to avoid redownloading historical returns on every workflow run. Source snapshots and timestamps are recorded; missing or stale data causes a controlled refresh or a logged error.
