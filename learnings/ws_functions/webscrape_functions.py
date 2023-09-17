# Import needed modules/libraries
import requests
from bs4 import BeautifulSoup


url = "https://www.skysports.com/premier-league-table"


def get_soup(url):
    """This returns the html data from a website using requests and beautifulsoup."""
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup


def get_table(soup):
    """This function returns data from a table."""
    league_data = []
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


soup_data = get_soup(url)
table_data = get_table(soup_data)
print(table_data)
