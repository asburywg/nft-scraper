import json

from common.operations import clean_twitter_username
from common.s3 import generate_s3_path, s3_put_json
from etl.load import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)


def percent_change(df, date_col, group_by_col, calculate_col):
    df[date_col] = pd.to_datetime(df[date_col])
    df.sort_values([group_by_col, date_col], inplace=True, ascending=[True, True])
    df[f'{calculate_col}_perc'] = df.groupby(group_by_col)[calculate_col].apply(pd.Series.pct_change)
    print(df.groupby(group_by_col)[f'{calculate_col}_perc'].mean().sort_values(ascending=False))
    return df


def export_csv(df, filename, directory="data"):
    df.to_csv(f"./{directory}/{filename}.csv", index=False)


"""
load functions for sources by name: RARITY/TWITTER/OPENSEA
"""
# print(load_date("TWITTER", "20220522"))
twtr = load_all_dates("TWITTER")
print(percent_change(twtr, "date", "username", "followers_count"))


"""
merge functions
"""


def merge(date):
    # load rarity
    rarity = s3_read_json(S3_BUCKET, f'rarity/{date}/collections.json')
    df_rarity = pd.json_normalize(rarity)
    df_rarity['details.twitter_username'] = df_rarity['details.twitter_username'].apply(
        lambda x: clean_twitter_username(x))
    df_rarity['twtr_uname'] = df_rarity['details.twitter_username'].apply(lambda x: x.lower() if x else None)
    # load twitter
    twitter = s3_read_json(S3_BUCKET, f'twitter/{date}/profiles.json')
    df_twitter = pd.json_normalize(twitter)
    df_twitter['twtr_uname'] = df_twitter['username'].apply(lambda x: x.lower() if x else None)
    # merge
    df = pd.merge(df_rarity, df_twitter, how="left", on=['twtr_uname'])
    # persist
    result = json.loads(df.to_json(orient="records"))
    s3_path = generate_s3_path("combined", "projects.json")
    s3_put_json(result, S3_BUCKET, s3_path)


def merge_all_overlapping():
    rarity_dates = get_prefix_dates(S3_BUCKET, 'rarity')
    twitter_dates = get_prefix_dates(S3_BUCKET, 'twitter')
    merge_dates = [date for date in twitter_dates if date in rarity_dates]
    for date in merge_dates:
        merge(date)


