from enum import Enum
from common.s3 import s3_read_json, get_prefix_dates
import pandas as pd
from datetime import datetime

S3_BUCKET = "nft-data-tracker"


class SourceFilePath(Enum):
    RARITY = "rarity/{date}/collections.json"
    TWITTER = "twitter/{date}/profiles.json"
    OPENSEA = "opensea/{date}/details.json"


class Prefixes(Enum):
    RARITY = "rarity"
    TWITTER = "twitter"
    OPENSEA = "opensea"


"""
load functions
"""


def load_raw_json(date: str, filepath: SourceFilePath, max_level=None):
    f = filepath.value.replace("{date}", date)
    raw = s3_read_json(S3_BUCKET, f)
    df = pd.json_normalize(raw, max_level=max_level)
    df['date'] = datetime.strptime(date, '%Y%m%d')
    return df


def load_rarity_clean(date: str):
    df = load_raw_json(date, SourceFilePath.RARITY, 0)
    df = df.drop(['seven_day_volume'], axis=1, errors='ignore')  # duplicate in stats
    if 'details' in list(df.columns):
        df['twitter_username'] = pd.json_normalize(data=df['details'])['twitter_username']
    stats = pd.json_normalize(data=df['stats'])
    concat = pd.concat([df, stats], axis=1)
    remove_columns = ['image_url', 'details', 'stats', 'id', 'contracts',
                      'floor_price']  # floor_price is 0 for all rows
    df = concat.drop(remove_columns, axis=1, errors='ignore')
    df.reset_index(inplace=True, drop=True)
    return df


def load_twitter_clean(date: str):
    df = load_raw_json(date, SourceFilePath.TWITTER, 0)
    public_metrics = pd.json_normalize(data=df['public_metrics'])
    concat = pd.concat([df, public_metrics], axis=1)
    remove_columns = ['entities', 'protected', 'description', 'id', 'name', 'pinned_tweet_id', 'url',
                      'profile_image_url', 'public_metrics', 'location']
    df = concat.drop(remove_columns, axis=1, errors='ignore')
    return df


def load_opensea_clean(date: str):
    df = load_raw_json(date, SourceFilePath.OPENSEA, 1)
    stats = pd.json_normalize(data=df['collection.stats'])
    concat = pd.concat([df, stats], axis=1)
    remove_columns = ['collection.wiki_url', 'collection.is_nsfw', 'collection.dev_buyer_fee_basis_points',
                      'collection.dev_seller_fee_basis_points', 'collection.featured', 'collection.featured_image_url',
                      'collection.hidden', 'collection.safelist_request_status', 'collection.image_url',
                      'collection.only_proxied_transfers', 'collection.opensea_buyer_fee_basis_points',
                      'collection.opensea_seller_fee_basis_points', 'collection.payout_address',
                      'collection.is_subject_to_whitelist', 'collection.large_image_url', 'collection.discord_url',
                      'collection.display_data', 'collection.external_url', 'collection.editors',
                      'collection.payment_tokens', 'collection.primary_asset_contracts', 'collection.traits',
                      'collection.stats', 'collection.banner_image_url', 'collection.chat_url',
                      'collection.default_to_fiat', 'collection.description', 'error', 'collection.instagram_username',
                      'collection.telegram_url', 'collection.short_description', 'collection.require_email',
                      'collection.medium_username']
    df = concat.drop(remove_columns, axis=1, errors='ignore')
    return df


"""
date range functions
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


def load_date(name, dt):
    func = get_clean_load_func(name)
    return func(dt)


def load_all_dates(name):
    dt_range = get_prefix_dates(S3_BUCKET, Prefixes.__members__.get(name).value)
    func = get_clean_load_func(name)
    results = [func(dt) for dt in dt_range]
    return pd.concat(results)
