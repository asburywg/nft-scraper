import cloudscraper
from concurrent.futures import ThreadPoolExecutor
from common.operations import timing
from common.s3 import s3_read_json, s3_put_json, generate_s3_path

S3_BUCKET = "nft-data-tracker"
SLUG_FILES = ['opensea/slugs.json', 'rarity/slugs.json']

scraper = cloudscraper.create_scraper()


def get_project_details(slug):
    url = f"https://api.opensea.io/collection/{slug}?format=json"
    try:
        res = scraper.get(url, timeout=3)
        if res.status_code != 200:
            return {'error': res.text}
        return res.json()
    except Exception as e:
        return {'error': str(e)}


@timing
def multiprocess_fetch_details(slugs, workers=2):
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(get_project_details, slug) for slug in slugs]
        result = [future.result() for future in futures]
    return result


def get_twitter_usernames(results):
    usernames = []
    for x in results:
        nft = x.get('collection')
        if nft:
            usernames.append(nft.get('twitter_username'))
    return list(filter(None, usernames))


def lambda_handler(event, context):
    # get unique slugs from rarity, opensea, etc.
    slugs = []
    for filename in SLUG_FILES:
        slugs.extend(s3_read_json(S3_BUCKET, filename))
    unique_slugs = list(set(slugs))
    print(f"{len(slugs) - len(unique_slugs)} overlapping slugs, scraping {len(unique_slugs)} projects...")

    # fetch opensea project details
    results = multiprocess_fetch_details(slugs)
    s3_put_json(results, S3_BUCKET, generate_s3_path("opensea", "details.json"))

    # persist unique twitter usernames found in projects
    usernames = get_twitter_usernames(results)
    s3_put_json(list(set(usernames)), S3_BUCKET, "opensea/twitter.json")


# lambda_handler(None, None)
