### OBSOLETE ###

# Import needed modules
import requests
from bs4 import BeautifulSoup
import smtplib

# Declare URLs of product you wish to buy
url_cpu = "https://www.scan.co.uk/products/amd-ryzen-5-3600-am4-zen-2-6-core-12-thread-36ghz-42ghz-turbo-32mb-l3-pcie-40-65w-cpu-pluswraith-ste"
url_motherboard = "https://www.scan.co.uk/products/msi-b450-tomahawk-max-amd-b450-s-am4-ddr4-sata3-m2-2-way-crossfire-realtek-gbe-usb-32-gen2-aplusc-at"
url_ram = "https://www.scan.co.uk/products/16gb-2x8gb-corsair-ddr4-vengeance-lpx-black-pc4-25600-3200-non-ecc-unbuff-cas-16-135v-amd-ryzen-opti"


# Create functions


def get_price(url):
    """This function returns the price of a product from the URL (SCAN platform) provided."""
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "html.parser")
    price = soup.find("span", {"itemprop": "price"})["content"]
    return price


def add_prices(*args):
    """This function adds the prices of the inputs and returns the total."""
    total = 0
    for arg in args:
        total += float(arg)
    return total


def send_mail(total_price):
    """This function sends an email message updating the receiver of the price upgrade total."""
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("yourgmail@gmail.com", "yourpassword")
    subject = "Your Upgrade Price Today"
    body = f"The total price to upgrade today is: {total_price}"
    message = f"Subject:{subject}\n\n{body}"
    server.sendmail("email_from@gmail.com", "email_to@gmail.com", message)
    print("Email sent...")
    server.quit()
