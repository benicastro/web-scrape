# Extracting Images and Associated Texts from Twitter through Keywords Search

import datetime
import random
import pandas as pd
import gspread
import itertools
import requests

from pyspark.sql.functions import col
from pyspark.sql.types import DateType


@dataclass
class ImageText:
    search_keyword: str | None
    source_link: str | None
    date: str | None
    date_posted: str | None
    media_url: list | None
    text: str | None
    platform: str | None


class Twitter_RapidAPI:
    def __init__(self):
        self.api_key = ""
        self.base_url = "https://twitter154.p.rapidapi.com"
        self.host = "twitter154.p.rapidapi.com"

    def keyword_tweets(
        self,
        query,
        section="latest",
        limit="20",
        max_pages=100,
        start_date="2022-01-01",
        language="en",
    ):
        url = f"{self.base_url}/search/search"
        querystring = {
            "query": query,
            "section": section,
            "limit": limit,
            "start_date": start_date,
            "language": language,
        }
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host,
        }
        return self._get_tweets(url, querystring, headers, max_pages)

    def _get_tweets(self, url, querystring, headers, max_pages):
        tweets = []
        continuation_token = None
        page_counter = 0
        previous_continuation_token = None

        while True:
            if continuation_token:
                new_url = "https://twitter154.p.rapidapi.com/search/search/continuation"
                url = new_url
                querystring["continuation_token"] = continuation_token

            response = requests.request("GET", url, headers=headers, params=querystring)
            data = response.json()
            try:
                for tweet in data["results"]:
                    tweets.append(tweet)
            except KeyError:
                try:
                    print(
                        f"No tweets found. API Response: '{response.json()['message']}'."
                    )  # API gave a response message
                    break
                except KeyError:
                    print(
                        f"No tweets found. API Response: '{response.json()}'."
                    )  # Could be a different case.
                    break
                except Exception as e:
                    print(f"An error occured: {e}")
            except Exception as e:
                print(f"An error occured: {e}")
            continuation_token = data.get("continuation_token")
            page_counter += 1
            print(f"Parsing Page {page_counter}.")

            if continuation_token == None or page_counter >= max_pages:
                print(f"{len(tweets)} tweets retrieved.")
                break

            if previous_continuation_token == continuation_token:
                print("Duplicate continuation token found. Stopping loop.")
                break

            previous_continuation_token = continuation_token

        return tweets


class SheetsUtils:
    def __init__(self, creds_path=""):
        self.creds_path = creds_path

    def gs_to_dict(self, tab_name, spreadsheet_id):
        gc = gspread.service_account(filename=self.creds_path)
        sh = gc.open_by_key(spreadsheet_id)
        wks = sh.worksheet(tab_name)
        results_json = wks.get_all_records()
        return results_json

    def gs_to_df(self, tab_name, spreadsheet_id):
        json_data = self.gs_to_dict(tab_name, spreadsheet_id)
        gspread_result = sc.parallelize(json_data).toDF()
        return gspread_result

    def gs_to_list(self, tab_name, spreadsheet_id, relevant_key):
        json_data = self.gs_to_dict(tab_name, spreadsheet_id)
        results_list = [result[relevant_key] for result in json_data]
        return results_list


def flatten_list(list_input):
    """This function flattens a list of lists input and returns a single list with no empty string elements."""
    flat_list = [item for sublist in list_input for item in sublist]
    return list(filter(None, flat_list))


def parse_creation_date(date_string):
    """This function parses an input date in string format and converts it into a specific form."""
    date_format = "%a %b %d %H:%M:%S %z %Y"
    parsed_date = datetime.datetime.strptime(date_string, date_format).date()
    return parsed_date


def get_entry(keyword, post_link, date, date_posted, media_link, text, platform):
    """This function creates an entry for the output data with the recommended schema using information from the website."""
    new_entry = ImageText(
        search_keyword=keyword,
        source_link=post_link,
        date=date,
        date_posted=date_posted,
        media_url=media_link,
        text=text,
        platform=platform,
    )
    return new_entry


# Sheet credentials
tab_name = "Boolean Searches"
spreadsheet_id = "1PjA457fCHZwu5F68EHokCLv3ZA4wa1u-3hF-zZ2qvzg"

# Check dataframe
sheet = SheetsUtils()
df_sheet = sheet.gs_to_df(tab_name, spreadsheet_id)
df_sheet.display()


static_keyword_list = []
english_keyword_list = []

static_search_list = sheet.gs_to_list(
    tab_name, spreadsheet_id, "Static Searches (English)"
)
english_search_list = sheet.gs_to_list(tab_name, spreadsheet_id, "English")

for i in range(len(static_search_list)):
    row_static = re.sub(r"[()]", "", static_search_list[i])
    if (
        row_static.count("AND") > 1
    ):  # Case where there is an additional AND condition in the search query
        kw1 = [x.strip() for x in row_static.split("AND")[0].split("OR")]
        kw2 = [x.strip() for x in row_static.split("AND")[-2].split("OR")]
        static_keywords = [f"{a} {b}" for a, b in itertools.product(kw1, kw2)]
    else:
        static_keywords = [x.strip() for x in row_static.split("AND")[0].split("OR")]
    static_keyword_list.append(static_keywords)

for j in range(len(english_search_list)):
    row_english = re.sub(r"[()]", "", english_search_list[j])
    if "AND" in row_english:
        english_keywords = [" ".join(row_english.split(" AND "))]
    else:
        english_keywords = row_english.split(" OR ")
    english_keyword_list.append(english_keywords)

# Combine into a single list and remove empty strings from list
static_keyword_list = flatten_list(static_keyword_list)
english_keyword_list = flatten_list(english_keyword_list)

# Create a new list with all permutations of the previous two lists
kws = [
    f"{a} {b}" for a, b in itertools.product(static_keyword_list, english_keyword_list)
]


tw = Twitter_RapidAPI()
platform = "twitter"
language = "en"

# Create list to store scraped information
search_results = []

# scraped_posts = 0
# max_posts = 20
max_pages = 20  # 20 tweets per page

# Loop through all url sources
for keyword in [kws[0]]:
    # Get collection date
    date = datetime.date.today().strftime("%Y-%m-%d")

    item_results = tw.keyword_tweets(
        query=keyword, max_pages=max_pages, language=language
    )

    if not item_results:
        continue

    for result in item_results:
        if not result["media_url"]:
            continue

        query_kw = keyword

        try:
            post_id = result["tweet_id"]
            post_username = result["user"]["username"]
            post_link = f"https://twitter.com/{post_username}/status/{post_id}"
        except KeyError:
            post_link = "null"

        try:
            post_date = parse_creation_date(result["creation_date"])
        except KeyError:
            post_date = "null"

        try:
            post_text = result["text"]
        except KeyError:
            post_text = "null"

        try:
            post_media = result["media_url"]
        except KeyError:
            post_media = "null"

        entry = get_entry(
            keyword=query_kw,
            post_link=post_link,
            date=date,
            date_posted=post_date,
            media_link=post_media,
            text=post_text,
            platform=platform,
        )

        search_results.append(asdict(entry))

        # scraped_posts += 1
        # if scraped_posts >= max_posts:
        #   break

    time.sleep(random.randint(1, 5))  # Limit request frequency
