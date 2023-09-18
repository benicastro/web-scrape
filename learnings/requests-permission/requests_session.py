# Import needed modules/libraries
import requests
from bs4 import BeautifulSoup
import credentials

# Set website url to access
login_url = "https://the-internet.herokuapp.com/authenticate"
secure_url = "https://the-internet.herokuapp.com/secure"

# Create payload
payload = {
    "username": credentials.username,
    "password": credentials.password,
}

# Perform requests with a context manager
with requests.session() as s:
    s.post(login_url, data=payload)
    r = s.get(secure_url)
    soup = BeautifulSoup(r.text, "html.parser")
    print(soup.prettify())
