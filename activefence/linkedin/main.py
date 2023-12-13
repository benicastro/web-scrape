import requests

url = "https://linkedin-profiles1.p.rapidapi.com/extract"

querystring = {"url": "https://ca.linkedin.com/in/paulmeade", "html": "1"}

headers = {
    "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
    "X-RapidAPI-Host": "linkedin-profiles1.p.rapidapi.com",
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
