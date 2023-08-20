import requests
from bs4 import BeautifulSoup

url = "https://www.skysports.com/premier-league-table"
r = requests.get(url)

soup = BeautifulSoup(r.text, "html.parser")

league_table = soup.find("tbody")

for row in league_table.find_all("tr"):
    team = row.find_all("td")[1].text.strip()
    print(team)
