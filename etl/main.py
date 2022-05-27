from etl.load import *
from common.s3 import *
from common.operations import *
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 1)

dt = '20220505'

"""
explore functions
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


"""
helper functions
"""


def export_csv(df, filename, directory="data"):
    df.to_csv(f"./{directory}/{filename}.csv", index=False)


"""
load raw functions
"""


def load_date_raw(fp: FilePath, date: str, export: bool = False, log: bool = False):
    df = load_raw_json(date, fp)
    print(fp.name)
    if log:
        print(df)
    if export:
        export_csv(df, f"{fp.name}-{date}")


# load_date_raw(FilePath.OPENSEA, dt, True)


def load_date_raw_all(date: str, export: bool = False, log: bool = False):
    for val in FilePath:
        load_date_raw(val, date, export, log)


# load_date_raw_all(dt, True)


"""
load cleaned functions
"""


FUNCTIONS = {"RARITY": load_rarity_clean, "TWITTER": load_twitter_clean, "OPENSEA": load_opensea_clean}


def get_clean_load_func(name):
    # Python > 3.10 pattern matching
    # match name:
    #     case "RARITY":
    #         return load_rarity_clean
    #     case "TWITTER":
    #         return load_twitter_clean
    return FUNCTIONS.get(name)


def load_full_clean(export: bool = False, log: bool = False):
    for val in FilePath:
        dt_range = get_prefix_dates(S3_BUCKET, Prefixes.__members__.get(val.name).value)
        print(f"{val.name}: loading {len(dt_range)} dates")
        load_func = get_clean_load_func(val.name)
        frames = [load_func(dt) for dt in dt_range]
        df = pd.concat(frames)
        if log:
            print(df)
        if export:
            export_csv(df, f"{val.name}-full")


# load_full_clean(True, True)


def export_clean_full(fp: FilePath):
    dt_range = get_prefix_dates(S3_BUCKET, Prefixes.__members__.get(fp.name).value)
    print(f"{fp.name}: loading {len(dt_range)} dates")
    load_func = get_clean_load_func(fp.name)
    frames = [load_func(date) for date in dt_range[1:]]  # first opensea file malformat
    df = pd.concat(frames)
    export_csv(df, f"{fp.name}-full")


def export_all_clean_full():
    for val in FilePath:
        export_clean_full(val)


export_clean_full(FilePath.OPENSEA)
# export_all_clean_full()
