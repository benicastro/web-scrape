# Import needed modules
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Set website url to scrape
url = "https://www.skysports.com/premier-league-table"


# Create function
def scrape_tables(url_to_scrape):
    """This function scrapes data scores from a table given a website url."""

    league_data = []

    req = requests.get(url_to_scrape)
    soup = BeautifulSoup(req.text, "html.parser")

    league_table = soup.find("tbody")
    for row in league_table.find_all("tr"):
        team = row.find_all("td")[1].text.strip()
        points = row.find_all("td")[9].text.strip()
        team_data = {
            "name": team,
            "points": points,
        }
        league_data.append(team_data)

    return league_data


# Test function
data = scrape_tables(url)

# create data frame
league_df = pd.DataFrame(data)
league_df.to_csv("league_data.csv")
