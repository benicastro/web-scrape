# Extracting Images and Associated Texts from Instagram

# Import modules

import requests
import json
import re
from bs4 import BeautifulSoup
from uuid import uuid4
from pyspark.sql.functions import col
from functools import reduce
import datetime
import numpy as np
import time
import random
import pandas as pd

from dataclasses import dataclass, asdict

from pyspark.sql.functions import col
from pyspark.sql.types import DateType

# Schema


@dataclass
class ImageText:
    original_source_link: str | None
    source_link: str | None
    date_collected: str | None
    date_posted: str | None
    media_url: list | None
    text: str | None
    platform: str | None


# Fetch Data Collection Links

urls = [source if "http" in source else ("https://" + source) for source in sources]
urls

# Functions


def extract_instagram_username(url):
    """This function returns the username of the given instagram account url."""
    if "?" in url:
        url = url.split("?")[0]
    name = re.split("/", url)[-1]
    if name == "":
        name = re.split("/", url)[-2]
    return name


def get_uid_by_name_via_vetricio(username):
    """This function returns the user id of an instagram account given the username."""
    url = f"https://api.vetric.io/instagram/v1/users/{username}/usernameinfo"
    response = requests.request("GET", url, headers=HEADERS_VERTIC, data={})
    if response.status_code != 200:
        print("API request %s fails:" % url)
        print(response.status_code)
    else:
        json_data = response.json()
        uid = json_data["user"]["pk"]
    return uid


def get_user_feed(uid, querystring={"": ""}):
    """This function returns the user feed json data of an instagram account given the user id."""
    url = f"https://api.vetric.io/instagram/v1/feed/user/{uid}"
    response = requests.request(
        "GET", url, headers=HEADERS_VERTIC, data={}, params=querystring
    )
    json_data = response.json()
    return json_data


def get_entry(
    website_link, post_link, date_collected, date_posted, media_link, text, platform
):
    """This function creates an entry for the output data with the recommended schema using information from the website."""
    new_entry = ImageText(
        original_source_link=website_link,
        source_link=post_link,
        date_collected=date_collected,
        date_posted=date_posted,
        media_url=media_link,
        text=text,
        platform=platform,
    )
    return new_entry


# Main

# Create list to store scraped information
website_data = []
platform = "instagram"
# Loop through all url sources
for url in urls:
    # Get collection date
    date_collected = datetime.date.today().strftime("%Y-%m-%d")
    print(f"Extracting information from source: {url} ...", end=" ")

    # Get username and user id
    max_retries = 3
    retry_count = 0
    need_retry = True
    while (need_retry) & (retry_count <= 3):
        try:
            username = extract_instagram_username(url)
            uid = get_uid_by_name_via_vetricio(username)
            need_retry = False
        except UnboundLocalError:
            retry_count += 1
            print(retry_count)
            time.sleep(10)

    # Set number of posts to be scraped per user
    max_posts = 100

    more_posts = True
    scraped_posts = 0
    querystring = {"": ""}

    while (more_posts) & (scraped_posts < max_posts):
        # Get json data
        json_data = get_user_feed(uid, querystring)

        if "items" in json_data.keys():
            for i in range(len(json_data["items"])):
                post_info = json_data["items"][i]

                try:
                    post_code = post_info["code"]
                    post_link = f"https://www.instagram.com/p/{post_code}/"
                except KeyError:
                    post_link = "null"

                try:
                    post_date = datetime.datetime.fromtimestamp(
                        post_info["taken_at"]
                    ).strftime("%Y-%m-%d")
                except KeyError:
                    post_date = "null"

                try:
                    post_text = post_info["caption"]["text"]
                except (KeyError, TypeError):
                    post_text = "null"

                try:
                    if "video_versions" in post_info.keys():
                        post_media = post_info["video_versions"][0]["url"]
                    else:
                        post_media = post_info["image_versions2"]["candidates"][0][
                            "url"
                        ]
                except KeyError:
                    post_media = "null"

                entry = get_entry(
                    website_link=url,
                    post_link=post_link,
                    date_collected=date_collected,
                    date_posted=post_date,
                    media_link=post_media,
                    text=post_text,
                    platform=platform,
                )

                website_data.append(asdict(entry))

                scraped_posts += 1
                if scraped_posts >= max_posts:
                    break

            more_posts = json_data["more_available"]
            try:
                next_max_id = json_data["next_max_id"]
                querystring = {"max_id": f"{next_max_id}"}
            except KeyError:
                pass

        time.sleep(random.randint(1, 5))  # Limit request frequency per page

    print("Done!")

    time.sleep(random.randint(1, 5))  # Limit request frequency
