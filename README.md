# rarity.tools
* Lambda: `nft-scraper-rarity`
* Schedule: `0 20 * * ? *` (daily at 4PM EST)
* Outputs:
  * (override) Project slugs: `s3://nft-data-tracker/rarity/slugs.json`
  * (override) Twitter usernames: `s3://nft-data-tracker/rarity/twitter.json`
  * **Project details**: `s3://nft-data-tracker/rarity/{YYYYMMDD}/collections.json`

---

# OpenSea Rankings
* Lambda: `None` (runs locally with crontab)
* Schedule: `0 * * * *` (every hour)
  * Optimistic scheduling: cron jobs run while the computer is on & not sleeping
```
crontab -l
0 * * * * /usr/local/bin/python3 /Users/will/innanet3/nft-scraper/opensea/rankings/rankings.py
```
* Outputs:
  * (override) Project slugs: `s3://nft-data-tracker/opensea/slugs.json`
  * **Project rankings by volume**: `s3://nft-data-tracker/opensea/{YYYYMMDD}/{HH}/rankings.json`

---

# OpenSea Details
* Lambda: `nft-scraper-opensea-details`
* Schedule: `cron(30 20 * * ? *)` (daily at 4:30PM EST)
* Inputs:
  * `rarity/slugs.json`
  * `opensea/slugs.json`
* Outputs:
  * (override) Twitter usernames: `s3://nft-data-tracker/opensea/twitter.json`
  * **Project details**: `s3://nft-data-tracker/opensea/{YYYYMMDD}/details.json`
  
---

# Twitter
* Lambda: `nft-scraper-twitter`
* Schedule: `cron(0 21 * * ? *)` (daily at 5PM EST)
* Inputs: 
  * `rarity/twitter.json`
  * `opensea/twitter.json`
* Outputs:
  * Project details: `s3://nft-data-tracker/twitter/{YYYYMMDD}/profiles.json`
  
---

# nonfungible.com Market Data
* Lambda: `None` (runs locally with crontab)
* Schedule: `0 22 * * *` (daily at 6PM EST)
  * Optimistic scheduling: cron jobs run while the computer is on & not sleeping
  * Default timeframe of 1 month's data
```
crontab -l
0 22 * * * /usr/local/bin/python3 /Users/will/innanet3/nft-scraper/nonfungible/market_data.py
```
* Outputs:
  * Market statistics (monthly data): `s3://nft-data-tracker/nonfungible/{YYYYMMDD}/statistics.json`
  * (optional, manual) Market statistics (all-time data): `s3://nft-data-tracker/nonfungible/{YYYYMMDD}/statistics-full.json`

---

# Merge - DISABLED
* Lambda: `nft-scraper-merge`
* Schedule: `cron(30 21 * * ? *)` (daily at 5:30PM EST)
* Inputs: 
  * `rarity/{YYYYMMDD}/collections.json`
  * `opensea/{YYYYMMDD}/details.json`
  * `twitter/{YYYYMMDD}/profiles.json`
* Outputs:
  * Combined data: `s3://nft-data-tracker/combined/20220409/projects.json`

---
