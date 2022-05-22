import requests
from concurrent.futures import ThreadPoolExecutor
from common.operations import timing, clean_twitter_username
from common.s3 import s3_put_json, generate_s3_path

COLLECTIONS_STATS_ENDPOINT_URL = "https://collections.rarity.tools/collectionsStats"
COLLECTION_DETAILS_ENDPOINT_URL = "https://collections.rarity.tools/collectionDetails"
S3_BUCKET = "nft-data-tracker"


def fetch(url):
    res = requests.get(url)
    return res.json()


def mp_join_metadata(slug):
    url = f"{COLLECTION_DETAILS_ENDPOINT_URL}/{slug}"
    metadata = fetch(url)
    return metadata


@timing
def multiprocess_fetch_details(slugs, workers=10):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(mp_join_metadata, slug) for slug in slugs]
        result = [future.result() for future in futures]
    return result


def extract_twitter_usernames(results):
    twitter_filename = "rarity/twitter.json"
    twitter_usernames = list(set(filter(None, [clean_twitter_username(x.get('details').get('twitter_username')) for x in results])))
    print(f"{len(twitter_usernames)} Twitter usernames found. Overriding s3://{S3_BUCKET}/{twitter_filename}")
    s3_put_json(twitter_usernames, S3_BUCKET, twitter_filename)


@timing
def scrape_rarity_tools():
    # rarity.tools collection details
    s3_path = generate_s3_path("rarity", "collections.json")
    collections = fetch(COLLECTIONS_STATS_ENDPOINT_URL)
    slugs = [x['slug'] for x in collections]
    s3_put_json(slugs, S3_BUCKET, "rarity/slugs.json")
    print(f"Fetching details for {len(slugs)} projects...")
    results = multiprocess_fetch_details(slugs)
    print(f"Writing results to s3://{S3_BUCKET}/{s3_path}")
    s3_put_json(results, S3_BUCKET, s3_path)
    # project Twitter usernames
    extract_twitter_usernames(results)


def lambda_handler(event, context):
    scrape_rarity_tools()


# lambda_handler(None, None)
