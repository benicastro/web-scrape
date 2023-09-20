import requests

url = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/2023-09-20"

payload = ""
headers = {
    "authority": "api.sofascore.com",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "max-age=0",
    "if-none-match": "W/^\^fe179e759c^^",
    "origin": "https://www.sofascore.com",
    "referer": "https://www.sofascore.com/",
    "sec-ch-ua": "^\^Chromium^^;v=^\^116^^, ^\^Not",
}

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)
