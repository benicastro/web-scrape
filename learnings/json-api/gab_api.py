import requests

gab_url = "https://gab.com/api/v1/account_by_username/worth__fighting__for"

querystring = {"": ""}

payload = ""
headers = {
    "cookie": "_cfuvid=eHovyXkVzYfmam4pEmLObPqyGIG3qKcUDusaXSeUz7c-1695187463548-0-604800000; __cfruid=4d3c56cf5016cd5516f14554af45911c66f4aae7-1695187476; _gabsocial_session=EYNAQ8mxfyMI^%^2F7kRWeEpwQ74avBdIr3gkYC0^%^2Bc0r2GKH20OjdBe9OFYTx2bkbBt9BozH8Y0iD4guGbLEj7eMjJrx2ooFo9vP0W6yWlnyl7nK8^%^2FmF03UvX^%^2FBZZHdpX^%^2FDn8ue^%^2B83gXOGJ5UmBtpblSgZS4SqFvzay1i7kK^%^2BYzBONxiRZLX7fTLKXlkb2v6EtQdn8ZROKEsIsGh10Z7CTE1NqBQgXO1wiu8Ao6WT2GFfS9bCmtDq^%^2FBGFX29gKR7PIkxY4oIlEqBBi^%^2BXmSATv6tUroDZYjsOKExhbB2hy^%^2BWkMrgCp4rkUrtoXIwi4KR7L8lyQIQWaJ3WoYmXDvnQ^%^2Fim00DnY4gSsmKz58UTMF0KNMImXVRE0n4XE79shIPascQPyrGubP7UQCAtqipuvPKHpTt9a0aH2U04M--xaQ8uFaOoPccEqVm--rVrCAAUi4xWpt9pEXwEiMw^%^3D^%^3D",
    "authority": "gab.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.6",
    "if-none-match": "W/^\^2d7b1d8d36b682e73e4575e8474eb92b^^",
    "referer": "https://gab.com/",
    "sec-ch-ua": "^\^Brave^^;v=^\^117^^, ^\^Not",
}

response = requests.request(
    "GET",
    url="https://proxy.scrapeops.io/v1/",
    data=payload,
    headers=headers,
    params={
        "api_key": "9700bc2d-00dd-4930-8231-2427c294d51f",
        "url": gab_url,
    },
)

print(response.text)
