"""
Adapted from https://github.com/dcts/opensea-scraper using nodejs/puppeteer to python/bs4
Used to get project slugs from OpenSea rankings - used by opensea.details

Only works locally, error on lambda
`Detected a Cloudflare version 2 challenge, This feature is not available in the opensource (free) version.`

Run cron (works only when logged in) attempt every 30m
0 * * * * /usr/local/bin/python3 /Users/will/innanet3/nft-scraper/opensea/rankings/rankings.py
"""
import json
from bs4 import BeautifulSoup
import cloudscraper
import boto3
import datetime
from pytz import timezone
"""
ModuleNotFoundError: No module named 'common'
move needed function here (dupe)
"""

client = boto3.client('s3')


def s3_put_json(data, bucket, filename, prefix=None):
    client.put_object(Body=json.dumps(data), ContentType="application/json", Bucket=bucket,
                      Key=f'{prefix}/{filename}' if prefix else filename)


def get_date():
    tz = timezone('US/Eastern')
    return str(datetime.datetime.now(tz).date()).replace("-", "")


def generate_s3_path(prefix, filename, hour=False):
    if hour:
        return f"{prefix}/{get_date()}/{get_hour()}/{filename}"
    return f"{prefix}/{get_date()}/{filename}"


S3_BUCKET = "nft-data-tracker"
BROWSER = {'browser': 'firefox', 'platform': 'windows', 'mobile': False}
URLS = {"24h": "https://opensea.io/rankings?sortBy=one_day_volume",
        "7d": "https://opensea.io/rankings?sortBy=seven_day_volume",
        "30d": "https://opensea.io/rankings?sortBy=thirty_day_volume",
        "total": "https://opensea.io/rankings?sortBy=total_volume"}

scraper = cloudscraper.create_scraper(browser=BROWSER)


def get_hour():
    tz = timezone('US/Eastern')
    return str(datetime.datetime.now(tz).hour)


def scrape_page(url):
    try:
        soup = BeautifulSoup(scraper.get(url, timeout=5).text, 'html.parser')
        result = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).text)
        nodes = result.get('props').get('relayCache')[0][1].get('json').get('data').get('rankings').get('edges')
        return [node.get('node') for node in nodes]
    except Exception as e:
        print(f"Failed to scrape page {url}: {e}")


def scrape_opensea_rankings():
    rankings = {}
    for timeframe, url in URLS.items():
        print(f"Fetching rankings for {timeframe} volume...")
        rankings[timeframe] = scrape_page(url)
    return rankings


def get_unique_slugs(rankings):
    x = rankings.values()
    projects = sum(x, [])
    return list(set([x['slug'] for x in projects]))


def main():
    # OpenSea rankings for 24h, 7d, 30d, total timeframes
    rankings = scrape_opensea_rankings()
    s3_put_json(rankings, S3_BUCKET, generate_s3_path("opensea", "rankings.json", True))

    # get project details by unique slugs
    slugs = get_unique_slugs(rankings)
    print(f"{len(slugs)} unique projects found")
    s3_put_json(slugs, S3_BUCKET, "opensea/slugs.json")


main()