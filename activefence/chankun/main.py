####################################################################
# Extracting Images and Texts from 4chan  ##########################
# by Benedict Z. Castro | benedict.zcastro@gmail.com  ##############
####################################################################

# Import needed modules and libraries ##############################
import time
import pandas
import httpx
import random
from datetime import date
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict


# Schema ###########################################################
@dataclass
class ImageText:
    source_link: str | None
    date: str | None
    media_url: str | None
    text: str | None


# Fetch data links #################################################
with open("website_links.txt") as file:
    sources = file.read().split("\n")

urls = [source if "http" in source else ("https://" + source) for source in sources]


# Functions ########################################################
def get_html(url, **kwargs):
    """This function returns the HTML content of a given website url"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    if kwargs.get("page"):
        response = httpx.get(
            url + str(kwargs.get("page")), headers=headers, follow_redirects=True
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


def get_entry(website_link, date_collected, media_link, text):
    """This function creates an entry for the output data with the recommended schema using information from the website."""
    new_entry = ImageText(
        source_link=website_link,
        date=date_collected,
        media_url=media_link,
        text=text,
    )
    return new_entry


# Main #############################################################
def main():
    website_data = []
    for url in [urls[2]]:
        print(url)
        collection_date = date.today().strftime("%Y-%m-%d")  # Get collection date
        html = get_html(url)
        # print(html.html)

        if html is False:
            continue

        # media_nodes = extract_media(html, "div.thread")
        media_nodes = extract_media(html, "div.mix")

        for node in media_nodes:
            # media_link = node.css_first("a.fileThumb").attrs["href"]
            media_link = node.css_first("img.thread-image").attrs["src"]
            # print(media_link)

            try:
                # text = node.css_first("div.postInfo > span.subject").text()
                # text_subject = node.css_first("p.intro > span.subject").text()
                # text_node = node.css_first("div.replies")
                # te
                text = (
                    node.css_first("div.replies").text().strip().split("View thread")[1]
                )
            except KeyError:
                text = "null"
            # print(text)

            entry = get_entry(
                website_link=url,
                date_collected=collection_date,
                media_link=media_link,
                text=text,
            )

            website_data.append(asdict(entry))

        time.sleep(random.randint(1, 3))  # Limit request frequency

    print(website_data)


if __name__ == "__main__":
    main()


# Issues Found
# 1. Images like logos, backgrounds, etc
# 2. Images with no associated text
# 3. Images from source sets
# 4. Scrolling websites
# 5.
#
#
#
#
#
#
#
