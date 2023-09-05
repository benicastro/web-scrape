# Import modules/libraries
import mechanicalsoup
import pandas as pd
import sqlite3

# Define url
url = "https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions"

# Create browser object
browser = mechanicalsoup.StatefulBrowser()
browser.open(url)

# Extract table headers
th = browser.page.find_all("th", attrs={"class": "table-rh"})
distribution = [value.text.replace("\n", "") for value in th]
distribution = distribution[:98]

# Extract table data
td = browser.page.find_all("td")
columns = [value.text.replace("\n", "") for value in td]
columns = columns[6:1084]

# Select every 11th item
column_names = [
    "Founder",
    "Maintainer",
    "Initial_Release_Year",
    "Current_Stable_Version",
    "Security_Updates",
    "Release_Date",
    "System_Distribution_Commitment",
    "Forked_From",
    "Target_Audience",
    "Cost",
    "Status",
]

dict = {"Distribution": distribution}

for idx, key in enumerate(column_names):
    dict[key] = columns[idx:][::11]

df = pd.DataFrame(data=dict)

# Insert data into a database
connection = sqlite3.connect("linux_distro.db")
cursor = connection.cursor()

cursor.execute("create table linux (Distribution, " + ",".join(column_names) + ")")
for i in range(len(df)):
    cursor.execute("insert into linux values (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i])

connection.commit()
connection.close()
