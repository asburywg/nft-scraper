"""
nonfungible.com is blocked by cloudflare (captcha, cookies??)
unable to use cloudscraper
playwright works locally, not in lambda
converted to node on branch nonfungible, works locally but blocked in lambda

---
default is 1 months data, needs to successfully run cron at least once a month - else get all time data

Run cron (works only when logged in) attempt at 6PM EST daily
0 22 * * * /usr/local/bin/python3 /Users/will/innanet3/nft-scraper/nonfungible/market_data.py
"""

import json
from enum import Enum
from playwright.sync_api import sync_playwright
import boto3
from pytz import timezone
import datetime

client = boto3.client('s3')


def s3_put_json(data, bucket, filename, prefix=None):
    client.put_object(Body=json.dumps(data), ContentType="application/json", Bucket=bucket,
                      Key=f'{prefix}/{filename}' if prefix else filename)


def get_date():
    tz = timezone('US/Eastern')
    return str(datetime.datetime.now(tz).date()).replace("-", "")


def generate_s3_path(prefix, filename):
    return f"{prefix}/{get_date()}/{filename}"


"""
**statistics**
https://nonfungible.com/api/statistics?metrics[]=count-sale&metrics[]=sum-usd&metrics[]=avg-usd&metrics[]=unique-wallets&metrics[]=count-salesprimary&metrics[]=count-salessecondary&metrics[]=sum-usdprimary&metrics[]=sum-usdsecondary&metrics[]=unique-buyer&metrics[]=unique-seller&avg=X&limit=N

N = timeframe
- 1 week = 8
- 1 month = 31
- 3 month = 91
- 1 year = 366
- All time = 9007199254740992

X = moving average period
- Daily = 1
- Weekly = 7
- Monthly = 30
- Yearly = 365
- All time = alltime
"""


class Timeframe(Enum):
    WEEK = 8
    MONTH = 31
    QUARTER = 91
    YEAR = 366
    ALL_TIME = 9007199254740992


class MovingAverage(Enum):
    DAILY = 1
    WEEKLY = 7
    MONTHLY = 30
    YEARLY = 365
    ALL_TIME = "alltime"


S3_BUCKET = "nft-data-tracker"
DEFAULT_TIMEFRAME = Timeframe.MONTH
DEFAULT_MA = MovingAverage.DAILY


def playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.webkit.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            html = page.evaluate('document.querySelector("pre").innerText')
            return json.loads(html)
    except:
        return None


def scrape_market_data(all_time=False):
    # nonfungible.com statistics
    timeframe = Timeframe.ALL_TIME.value if all_time else DEFAULT_TIMEFRAME.value
    moving_average = DEFAULT_MA.value
    url = f"https://nonfungible.com/api/statistics?metrics[]=count-sale&metrics[]=sum-usd&metrics[]=avg-usd&metrics[]=unique-wallets&metrics[]=count-salesprimary&metrics[]=count-salessecondary&metrics[]=sum-usdprimary&metrics[]=sum-usdsecondary&metrics[]=unique-buyer&metrics[]=unique-seller&avg={moving_average}&limit={timeframe}"
    data = playwright(url)
    if data:
        s3_put_json(data, S3_BUCKET, generate_s3_path("nonfungible", "statistics-full.json" if all_time else "statistics.json"))


def main():
    scrape_market_data()


main()
