import time
import httpx
import random
import pandas as pd
import datetime

# from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urljoin
from selectolax.parser import HTMLParser
from dataclasses import dataclass, asdict
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pyspark.sql.functions import col
from pyspark.sql.types import DateType
from seleniumwire import webdriver


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
    """This function returns the HTML content of a given website url and page number."""
    # Configure browser
    s = Service("/tmp/chrome/latest/chromedriver_linux64/chromedriver")
    options = webdriver.ChromeOptions()
    options.binary_location = "/tmp/chrome/latest/chrome-linux/chrome"
    options.add_argument("--headless")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=8888")
    options.add_argument("--homedir=/tmp/chrome/chrome-user-data-dir")
    options.add_argument("--user-data-dir=/tmp/chrome/chrome-user-data-dir")
    PROXY = get_oxylabs_proxy()["https"]
    # print(PROXY)
    options.add_argument("--proxy-server=%s" % PROXY)
    prefs = {
        "download.default_directory": "/tmp/chrome/chrome-user-data-di",
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=s, options=options)
    time.sleep(5)
    driver.get(url)
    # Navigate through pages
    if kwargs.get("page") and kwargs.get("page") >= 2:
        page_number = str(kwargs.get("page"))
        page_element = driver.find_element(
            By.CSS_SELECTOR,
            value=f"div.gsc-cursor-page[aria-label='Page {page_number}']",
        )
        page_element.click()
        time.sleep(5)
        page_source = driver.page_source
    else:
        page_source = driver.page_source
    driver.close()
    html = HTMLParser(page_source)
    return html


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
for url in [urls[3]]:
    # Get collection date
    date_collected = datetime.date.today().strftime("%Y-%m-%d")

    # Specify platform
    platform = "4chan"

    max_page = 10

    for page in range(1, max_page + 1):
        # html = get_html(url, page=page)
        # print(html.html)
        try:
            html = get_html(url, page=page)
            # print(html.html)
        except:
            continue

        media_nodes = extract_media(html, "div.gsc-webResult.gsc-result")

        for node in media_nodes:
            try:
                date_posted = ""
            except KeyError:
                date_posted = "null"

            try:
                thread_link = node.css_first("a.gs-title").attrs["href"]
                # print(thread_link)
            except KeyError:
                thread_link = "null"

            try:
                media_link = node.css_first("img.gs-image").attrs["src"]
            except (KeyError, AttributeError):
                media_link = "null"

            try:
                post_title = node.css_first("a.gs-title").text()
                post_body = node.css_first("div.gs-bidi-start-align.gs-snippet").text()
                text = text = post_title + "\n" + post_body
            except KeyError:
                text = "null"

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

        time.sleep(random.randint(1, 3))
    time.sleep(random.randint(5, 10))  # Limit request frequency per url
