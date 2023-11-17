import time
import httpx
import random
import pandas as pd
import datetime
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
from pyspark.sql.functions import col
from pyspark.sql.types import DateType


@dataclass
class ImageText:
    original_source_link: str | None
    source_link: str | None
    date_collected: str | None
    date_posted: str | None
    media_url: str | None
    text: str | None
    platform: str | None


# Create list for website sources
with open(
    "/Workspace/Users/benedict@activefence.com/chankun/sample_websites.txt"
) as file:
    sources = file.read().split("\n")

urls = [source if "http" in source else ("https://" + source) for source in sources]
urls


def get_html(url, **kwargs):
    """This function returns the HTML content of a given website url"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    if kwargs.get("page"):
        response = httpx.get(
            url + "/" + str(kwargs.get("page")), headers=headers, follow_redirects=True
        )
    else:
        response = httpx.get(url, headers=headers, follow_redirects=True)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. \nPage Limit Exceeded..."
        )
        return False
    html = HTMLParser(response.text)
    return html
    # return response.text


def extract_media(website_html, selector):
    """This function return node objects given the html and the necessary css selector."""
    try:
        return website_html.css(selector)
    except AttributeError:
        return None


def get_entry(
    website_link, thread_link, date_collected, date_posted, media_link, text, platform
):
    """This function creates an entry for the output data with the recommended schema using information from the website."""
    new_entry = ImageText(
        original_source_link=website_link,
        source_link=thread_link,
        date_collected=date_collected,
        date_posted=date_posted,
        media_url=media_link,
        text=text,
        platform=platform,
    )
    return new_entry


website_data = []
for url in [urls[0]]:
    # Get collection date
    date_collected = datetime.date.today().strftime("%Y-%m-%d")

    # Specify platform
    platform = "4chan"

    max_page = 10

    for page in range(1, max_page + 1):
        if page == 1:
            html = get_html(url)
        else:
            html = get_html(url, page=page)
        # print(html.html)

        if html is False:
            continue

        media_nodes = extract_media(html, "div.thread")

        for node in media_nodes:
            try:
                unix_time = int(node.css_first("span.dateTime").attrs["data-utc"])
                date_posted = datetime.datetime.utcfromtimestamp(unix_time).strftime(
                    "%Y-%m-%d"
                )
            except KeyError:
                date_posted = "null"

            try:
                thread_link = url + "/" + node.css_first("a.replylink").attrs["href"]
            except KeyError:
                thread_link = "null"

            try:
                media_link = node.css_first("a.fileThumb").attrs["href"]
                # print(media_link)
            except KeyError:
                media_link = "null"

            try:
                post_title = node.css_first("div.postInfo > span.subject").text()
                post_body = node.css_first("blockquote.postMessage").text()
                text = post_title + "\n" + post_body
            except KeyError:
                text = "null"
            # print(text)

            entry = get_entry(
                website_link=url,
                thread_link=thread_link,
                date_collected=date_collected,
                date_posted=date_posted,
                media_link=media_link,
                text=text,
                platform=platform,
            )

            website_data.append(asdict(entry))

        time.sleep(random.randint(3, 5))  # Limit request frequency per page

    time.sleep(random.randint(5, 10))  # Limit request frequency per url
