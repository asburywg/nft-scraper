import os
from common.operations import timing, clean_twitter_username
from common.s3 import s3_read_json, s3_put_json, generate_s3_path
from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv

"""
Reads usernames from rarity scraper cached in `rarity/twitter.json`
Input file replaced on every run - lose twitter tracking after project is off of rarity tools top collections 

Twitter API:
- https://developer.twitter.com/en/portal/dashboard
- https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_user_context.py
- https://developer.twitter.com/en/docs/twitter-api/rate-limits
- https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by
"""

load_dotenv()

S3_BUCKET = "nft-data-tracker"
TWITTER_FILES = ['opensea/twitter.json', 'rarity/twitter.json']
TWITTER_API_KEY = os.environ.get("TWITTER_API_KEY")
TWITTER_API_SECRET = os.environ.get("TWITTER_API_SECRET")
TWITTER_ACCOUNT_ACCESS_TOKEN = os.environ.get("TWITTER_ACCOUNT_ACCESS_TOKEN")
TWITTER_ACCOUNT_ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCOUNT_ACCESS_TOKEN_SECRET")
TWITTER_API_USERS = "https://api.twitter.com/2/users/by"
USER_FIELDS = "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected," \
              "public_metrics,url,username,verified,withheld"

oauth = OAuth1Session(TWITTER_API_KEY, client_secret=TWITTER_API_SECRET,
                      resource_owner_key=TWITTER_ACCOUNT_ACCESS_TOKEN,
                      resource_owner_secret=TWITTER_ACCOUNT_ACCESS_TOKEN_SECRET)


def oauth_get(url, params):
    res = oauth.get(url, params=params)
    if res.status_code != 200:
        raise Exception("Request returned an error: {} {}".format(res.status_code, res.text))
    return res.json()


def paginate_users(users, max_per_page=100):
    twitter_results = []
    # paginate users into groups of 100
    for i in range(0, len(users), max_per_page):
        # clean usernames
        page = [clean_twitter_username(user) for user in users[i:i + max_per_page]]
        usernames = ','.join(page)
        # bulk user request
        params = {"usernames": usernames, "user.fields": USER_FIELDS}
        res = oauth_get(TWITTER_API_USERS, params).get("data")
        twitter_results.extend(res)
    return twitter_results


def read_usernames():
    usernames = []
    for filename in TWITTER_FILES:
        usernames.extend(s3_read_json(S3_BUCKET, filename))
    return list(set(usernames))


@timing
def fetch_twitter():
    # get user profiles
    usernames = read_usernames()
    print(f"Fetching Twitter profiles for {len(usernames)} usernames")
    results = paginate_users(usernames)

    # write results to S3
    s3_path = generate_s3_path("twitter", "profiles.json")
    print(f"Found {len(results)} profiles. Writing results to s3://{S3_BUCKET}/{s3_path}")
    s3_put_json(results, S3_BUCKET, s3_path)


def lambda_handler(event, context):
    fetch_twitter()


# lambda_handler(None, None)

"""
TODO: search for Twitter usernames of blanks
Twitter API search less reliable than google search
"""
# params = {"q": "Psychedelics Anonymous Genesis", "count": 1}
# res = oauth_get("https://api.twitter.com/1.1/users/search.json", params)

# url = f'https://customsearch.googleapis.com/customsearch/v1?q=Mooning%20Monkey%20Project&key={key}'
# print(requests.get(url).json())
