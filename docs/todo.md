

### Merge
- Fix merge job to combine data daily (date, slug, ...) for all datasets (rarity, opensea, twitter)
  - Read date files, append date as column, concat
  - Join or add by slug/username,date - columns for each should be appended
  - Key: slug, date
- Enable merge cron lambda
- Move merge job under nft-scraper 

### Load
- load all daily combined datasets into something queryable - BigQuery, Snowflake, etc.

### Analysis
- Group by slug, change delta over time
- Day over day % change in floor, volume, followers
- Correlation testing between columns, floor and followers, volume, etc
- ML find patterns in dataset correlated with increasing floor price