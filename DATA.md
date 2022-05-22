# nonfungible.com Market Data
`statistics.json`
```json
{
    "count-sale": [],
    "sum-usd": [],
    "avg-usd": [],
    "unique-wallets": [],
    "count-salesprimary": [],
    "count-salessecondary": [],
    "sum-usdprimary": [],
    "sum-usdsecondary": [],
    "unique-buyer": [],
    "unique-seller": []
}
```
where each is array contains:
```json
[["epoch_time", "value"], [1651017600000, 14040], ...]
```

# Twitter
`profiles.json`
```json
   {
        "verified": false,
        "created_at": "2021-03-23T20:16:05.000Z",
        "entities":
        {
            "url":
            {
                "urls":
                [
                    {
                        "start": 0,
                        "end": 23,
                        "url": "https://t.co/40XGaod5Vw",
                        "expanded_url": "http://cryptosaints.co",
                        "display_url": "cryptosaints.co"
                    }
                ]
            },
            "description":
            {
                "urls":
                [
                    {
                        "start": 47,
                        "end": 70,
                        "url": "https://t.co/R8ZRiQJ63O",
                        "expanded_url": "https://discord.gg/yb7stVVeSn",
                        "display_url": "discord.gg/yb7stVVeSn"
                    },
                    {
                        "start": 80,
                        "end": 103,
                        "url": "https://t.co/03BLAvND5D",
                        "expanded_url": "https://opensea.io/collection/the-crypto-saints",
                        "display_url": "opensea.io/collection/the…"
                    }
                ]
            }
        },
        "description": "🚨MINTING IS LIVE NOW! ENDING NOV 30TH🚨discord: https://t.co/R8ZRiQJ63O Opensea: https://t.co/03BLAvND5D",
        "username": "_cryptosaints",
        "url": "https://t.co/40XGaod5Vw",
        "protected": false,
        "pinned_tweet_id": "1456981161973096452",
        "name": "CryptoSaints NFT",
        "id": "1374454900684333063",
        "public_metrics":
        {
            "followers_count": 1236,
            "following_count": 37,
            "tweet_count": 940,
            "listed_count": 17
        },
        "profile_image_url": "https://pbs.twimg.com/profile_images/1434696648668499968/Wfoi4DAF_normal.jpg"
    }
```

# OpenSea Details
`details.json`
```json
    {
        "collection":
        {
            "editors":
            [
                "0x0239769a1adf4def9f07da824b80b9c4fcb59593"
            ],
            "payment_tokens":
            [
                {
                    "id": 13689077,
                    "symbol": "ETH",
                    "address": "0x0000000000000000000000000000000000000000",
                    "image_url": "https://openseauserdata.com/files/6f8e2979d428180222796ff4a33ab929.svg",
                    "name": "Ether",
                    "decimals": 18,
                    "eth_price": 1.0,
                    "usd_price": 2954.76
                },
                {
                    "id": 4645681,
                    "symbol": "WETH",
                    "address": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
                    "image_url": "https://openseauserdata.com/files/accae6b6fb3888cbff27a013729c22dc.svg",
                    "name": "Wrapped Ether",
                    "decimals": 18,
                    "eth_price": 1.0,
                    "usd_price": 2954.76
                },
                {
                    "id": 409484150,
                    "symbol": "APE",
                    "address": "0x4d224452801aced8b2f0aebe155379bb5d594381",
                    "image_url": "https://lh3.googleusercontent.com/mkqhiVl1_aEJWznOYPJjwKiZjWw4gUnGfBxMcPO96JYVBrlhGhyiPQX7YouGObqom5F_fJOnsalw3TK6nJ92Ijctkcw9egWMxVj6vqQ=s120",
                    "name": "ApeCoin",
                    "decimals": 18,
                    "eth_price": 0.0055084,
                    "usd_price": 16.13
                }
            ],
            "primary_asset_contracts":
            [
                {
                    "address": "0x19b86299c21505cdf59ce63740b240a9c822b5e4",
                    "asset_contract_type": "non-fungible",
                    "created_date": "2022-02-14T02:17:02.012047",
                    "name": "DEGEN TOONZ",
                    "nft_version": "3.0",
                    "opensea_version": null,
                    "owner": 217528289,
                    "schema_name": "ERC721",
                    "symbol": "TOONZ",
                    "total_supply": "0",
                    "description": "8888 degenerate TOONZ that double as a membership to an exclusive metaverse community with the power to build it from the ground up.",
                    "external_link": "https://degentoonz.io",
                    "image_url": "https://lh3.googleusercontent.com/bLRdXEC6KIRmFAWBAgppvqeYQUVojbsGzIJJGfyH-WWF57iqOOlZu-1I0v0GYyrG8C-p-sVjpCMOZMFw0oVExilWzJTDbOfLeKhl1w=s120",
                    "default_to_fiat": false,
                    "dev_buyer_fee_basis_points": 0,
                    "dev_seller_fee_basis_points": 600,
                    "only_proxied_transfers": false,
                    "opensea_buyer_fee_basis_points": 0,
                    "opensea_seller_fee_basis_points": 250,
                    "buyer_fee_basis_points": 0,
                    "seller_fee_basis_points": 850,
                    "payout_address": "0xb047464bd7c66d0553fe7ead00b8ab9a77fd0097"
                }
            ],
            "traits": {
              "Bag":
                {
                    "cross body": 494,
                    "degen crossbody": 504
                },
                "BAG":
                {
                    "backpack": 758,
                    "none": 7129
                }
            },
            "stats":
            {
                "one_day_volume": 282.6693215599999,
                "one_day_change": 7.113141718416159,
                "one_day_sales": 274.0,
                "one_day_average_price": 1.0316398597080287,
                "seven_day_volume": 570.9828637882715,
                "seven_day_change": 0.6950718886648946,
                "seven_day_sales": 671.0,
                "seven_day_average_price": 0.8509431651091975,
                "thirty_day_volume": 1476.04824577575,
                "thirty_day_change": -0.19890252256199603,
                "thirty_day_sales": 2225.0,
                "thirty_day_average_price": 0.6633924700115731,
                "total_volume": 8647.24709322014,
                "total_sales": 16392.0,
                "total_supply": 8888.0,
                "count": 8888.0,
                "num_owners": 3854,
                "average_price": 0.5275284951940056,
                "num_reports": 114,
                "market_cap": 7563.182851490547,
                "floor_price": 0.87
            },
            "banner_image_url": "https://lh3.googleusercontent.com/ZPytVnAKjTzssmE9IfeXZY8P_12b6kzkO8EPGAfIuLMakTLySt7ccn26mO6cWOJzEK1APy25xBmwqrlXvae3YDpD_EJF-CJy26OC=s2500",
            "chat_url": null,
            "created_date": "2022-02-15T22:08:54.841369",
            "default_to_fiat": false,
            "description": "8888 degenerate TOONZ that double as a membership to an exclusive metaverse community with the power to build it from the ground up.",
            "dev_buyer_fee_basis_points": "0",
            "dev_seller_fee_basis_points": "600",
            "discord_url": "https://discord.gg/degentoonz",
            "display_data":
            {
                "card_display_style": "contain"
            },
            "external_url": "https://degentoonz.io",
            "featured": false,
            "featured_image_url": "https://lh3.googleusercontent.com/trTQYcSX3mu38Zg8jG373YT-yeIGKAuBY4CufctFg_wahjNoArlFjuxiIN0htC-uIK14o9nBA9WmTeX6vOu2O47XejVTnNdhPQwLgw=s300",
            "hidden": false,
            "safelist_request_status": "approved",
            "image_url": "https://lh3.googleusercontent.com/bLRdXEC6KIRmFAWBAgppvqeYQUVojbsGzIJJGfyH-WWF57iqOOlZu-1I0v0GYyrG8C-p-sVjpCMOZMFw0oVExilWzJTDbOfLeKhl1w=s120",
            "is_subject_to_whitelist": false,
            "large_image_url": "https://lh3.googleusercontent.com/trTQYcSX3mu38Zg8jG373YT-yeIGKAuBY4CufctFg_wahjNoArlFjuxiIN0htC-uIK14o9nBA9WmTeX6vOu2O47XejVTnNdhPQwLgw=s300",
            "medium_username": null,
            "name": "DEGEN TOONZ COLLECTION",
            "only_proxied_transfers": false,
            "opensea_buyer_fee_basis_points": "0",
            "opensea_seller_fee_basis_points": "250",
            "payout_address": "0xb047464bd7c66d0553fe7ead00b8ab9a77fd0097",
            "require_email": false,
            "short_description": null,
            "slug": "degentoonz-collection",
            "telegram_url": null,
            "twitter_username": null,
            "instagram_username": "DegenToonz",
            "wiki_url": null,
            "is_nsfw": false
        }
    }
```

`twitter.json`
```json
["thugpugsnft", "wallstreetchads", "octohedz", ...]
```

# OpenSea Rankings
`rankings.json`
```json
{
  "24h": [],
  "7d": [],
  "30d": [],
  "total": []
}
```
each time duration contains a list of projects:
```json
{
            "createdDate": "2022-04-29T13:58:31.855081",
            "name": "Otherdeed for Otherside",
            "slug": "otherdeed",
            "logo": "https://lh3.googleusercontent.com/yIm-M5-BpSDdTEIJRt5D6xphizhIdozXjqSITgK4phWq7MmAU3qE7Nw7POGCiPGyhtJ3ZFP8iJ29TFl-RLcGBWX5qI4-ZcnCPcsY4zI=s120",
            "isVerified": true,
            "nativePaymentAsset":
            {
                "symbol": "ETH",
                "asset":
                {
                    "imageUrl": "https://openseauserdata.com/files/6f8e2979d428180222796ff4a33ab929.svg",
                    "id": "QXNzZXRUeXBlOjEzNjg5MDc3"
                },
                "id": "UGF5bWVudEFzc2V0VHlwZTo0Mg=="
            },
            "statsV2":
            {
                "floorPrice":
                {
                    "unit": "3.69",
                    "eth": "3.69"
                },
                "numOwners": 33777,
                "totalSupply": 97149,
                "sevenDayChange": 0,
                "sevenDayVolume":
                {
                    "unit": "214214.074770442413864657"
                },
                "oneDayChange": -0.29541364637768547,
                "oneDayVolume":
                {
                    "unit": "16711.783401107601093827"
                },
                "thirtyDayChange": 0,
                "thirtyDayVolume":
                {
                    "unit": "214214.074770442413864657"
                },
                "totalVolume":
                {
                    "unit": "214214.074770442413864657"
                }
            },
            "id": "Q29sbGVjdGlvblR5cGU6MTQwNzcyNTU=",
            "__typename": "CollectionType"
        }
```

`slugs.json`
```json
["fluf", "the-lunartics", "coolmans-universe", "zombieclub-token", ...]
```

# rarity.tools
`collections.json`
```json
[
    {
        "slug": "cryptojankyz",
        "image_url": "https://lh3.googleusercontent.com/t2-r0kOctD_bjnl4QkcUWea3RFnUeo4gi3A5yCH1U3R8-8B-VevuXS8In0qeKomCVITW0puDRuM_sVWLjBd0ZelW5yziMzrMtlpe=s120",
        "details":
        {
            "name": "SUPERPLASTIC: Cryptojankyz",
            "blockchain": "ETHEREUM",
            "created_date": "2021-07-13T04:06:19.864433",
            "description": "Amateur art thieves and professional psychopaths Janky & Guggimon have broken into Christie’s NYC and jacked 22 ultra-rare and ridiculously valuable CryptoJanky NFTs. Unfortunately, Janky got cross-faded on the way to the job and accidentally set off a booby trap, leveling the Christie’s Auction House and blowing all the NFTs to bits! The drunken duo narrowly escaped the popo, hauling all the broken NFTs with them. Unwilling to give up their dream of getting Kanye rich — or at least copping enough cash for tequila, nuggs, and tix to Coachella — they’ve busted out the super-glue, huffed it, then recombined the broken bits into 9,240 totally unique CryptoJanky NFTs.",
            "discord_url": "https://discord.gg/superplasticnft",
            "external_url": "https://jankyheist.com",
            "large_image_url": "https://lh3.googleusercontent.com/7lk1TecsBtSdkxnTW71ManJJz77g-HtV0ICGkAm6uSraquyg27S8UDFUqYjCYGYe_AB9mNDf0P0VABNk6YTLDt-P2qwDu8669-9bUA=s300",
            "banner_image_url": "https://lh3.googleusercontent.com/xD68d-FfbUTGYBtmucPcsRSS2F22Mvtw-4D2pP0EZwmbYsGgxS5aK5ZrEK6orVUZC-5Pik3Yhs4Cyw4Bqg0Us4tPq8iNG8zBgcVS=s2500",
            "medium_username": null,
            "twitter_username": "superplastic",
            "instagram_username": "superplastic"
        },
        "seven_day_volume": 38.98859989900001,
        "stats":
        {
            "one_day_volume": 3.0408999000000003,
            "one_day_change": -0.8294704549660444,
            "one_day_sales": 13,
            "one_day_average_price": 0.23391537692307696,
            "seven_day_volume": 38.98859989900001,
            "seven_day_change": 1.7734890663413392,
            "seven_day_sales": 149,
            "seven_day_average_price": 0.26166845569798663,
            "total_volume": 9584.054769877152,
            "total_sales": 17830,
            "total_supply": 13867,
            "num_owners": 5822,
            "average_price": 0.5375241037508217,
            "market_cap": 3628.5564751639804,
            "floor_price": 0
        }
    }
]
```

`slugs.json`
```json
["cryptojankyz", "slacker-duck-pond", "meebits", "cryptopunks", ...]
```

`twitter.json`
```json
["absurdarboretum", "Sorasdreamworld", ...]
```