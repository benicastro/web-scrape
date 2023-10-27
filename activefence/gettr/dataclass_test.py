import requests
import json
import random
import time
import pandas as pd
from datetime import date
from dataclasses import dataclass, asdict


@dataclass
class Post:
    original_source_link: str
    source_link: str | None
    text: str | None
    date: str
    media_url: str | None
    platform: str | None


user_links = [
    "https://gettr.com/user/valiantnews",
    "https://gettr.com/user/welovetrumpnoah",
    "https://www.gettr.com/user/newsatual",
    "https://www.gettr.com/user/jairbolsonaro2",
    "https://www.gettr.com/user/pauloguedessz",
    "https://gettr.com/user/bolsonaros2",
    "https://gettr.com/user/theraginpatriot?",
    "https://gettr.com/user/theraginpatriot",
    "https://gettr.com/user/npagnotta1776 ",
    "https://www.gettr.com/user/newsatual",
    "https://www.gettr.com/user/jairbolsonaro2",
    "https://www.gettr.com/user/pauloguedessz",
    "https://gettr.com/user/bolsonaros2",
    "https://gettr.com/user/unitedworldint",
    "https://gettr.com/user/relevantenews",
    "https://gettr.com/user/tiagodasilvatv ",
    "https://gettr.com/user/unitedworldint",
    "https://gettr.com/user/elamerican_",
    "https://gettr.com/user/afa2a",
    "https://gettr.com/user/mohameddiallolive",
    "https://gettr.com/user/welovetrumpnoah",
    "https://gettr.com/user/crossroads_josh",
    "https://gettr.com/user/3musketeers",
    "https://gettr.com/user/drtonyhinton",
    "https://gettr.com/user/statsjamie",
    "https://gettr.com/user/vowalesofficial",
    "https://gettr.com/user/tommyrobinson1",
    "https://gettr.com/user/redice",
    "https://gettr.com/user/activepatriotuk",
    "https://gettr.com/user/allansantosbr",
    "https://gettr.com/user/fernandocerimedo",
    "https://gettr.com/user/divizio1",
    "https://gettr.com/user/x22reportgettr",
    "https://gettr.com/user/antimaskersclub",
    "https://gettr.com/user/cobratate",
    "https://gettr.com/user/alexjones",
    "https://gettr.com/user/warroom",
    "https://gettr.com/user/stevebannon",
]

# Create a function for API and request handling


def get_response(user, offset):
    """This function takes in string and integer inputs, respectively, for the user and offset values and outputs a response object in json format."""

    # API endpoint handling
    url = f"https://api.gettr.com/u/user/{user}/posts"
    querystring = {
        "offset": f"{offset}",
        "max": "20",
        "dir": "fwd",
        "incl": "posts",
        "fp": "f_uo",
    }
    payload = ""
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    }

    # Request handling
    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring
    )

    return response


# Create a list to store all user posts info
posts = []
max_posts = 100

# Loop through all users
for link in user_links:
    collection_date = date.today().strftime("%Y-%m-%d")  # Get collection date
    user = link.split("/")[-1]
    print(f"Extracting posts info from user: {user}")

    # Loop through all post pages/batches (a single page contains 20 posts)
    for offset in range(0, max_posts, 20):
        # JSON handling
        data = json.loads(get_response(user, offset).text)

        # Extract post ids
        try:
            num_posts = len(data["result"]["data"]["list"])
            post_ids = [
                data["result"]["data"]["list"][x]["activity"]["pstid"]
                for x in range(num_posts)
            ]
        except KeyError:
            post_ids = []

        # Loop through all posts in a page
        for id in post_ids:
            # posts_info = {}
            # posts_info["post_id"] = id

            try:
                post_text = data["result"]["aux"]["post"][id]["txt"]
            except KeyError:
                post_text = "null"

            try:
                if "previmg" in data["result"]["aux"]["post"][id].keys():
                    media_url = data["result"]["aux"]["post"][id]["previmg"].strip()
                elif "imgs" in data["result"]["aux"]["post"][id].keys():
                    media_url = (
                        "https://media.gettr.com/"
                        + data["result"]["aux"]["post"][id]["imgs"][0].strip()
                    )
                else:
                    media_url = "null"
            except KeyError:
                media_url = "null"

            # posts.append(posts_info)
            new_post = Post(
                original_source_link=link,
                source_link=f"https://gettr.com/post/{id}",
                text=post_text,
                date=collection_date,
                media_url=media_url,
                platform="GETTR",
            )
            posts.append(asdict(new_post))

        time.sleep(random.randint(2, 4))  # Limit request frequency

    print("Done...")
