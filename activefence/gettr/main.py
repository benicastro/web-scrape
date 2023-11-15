####################################################################
# Gettr Data Extraction using APIs                    ##############
# by Benedict Z. Castro | benedict.zcastro@gmail.com  ##############
####################################################################

# Import needed modules and libraries ##############################
import requests
import json
import random
import time
import pandas as pd

# Create list for users ############################################
with open(".\sample_sources.txt") as file:
    urls = file.read().split("\n")

users = []

for url in urls:
    users.append(url.split("/")[-1])


# Define a function for API and request handling
def get_response(user, offset):
    # API endpoint handling
    url = f"https://api.gettr.com/u/user/{user}/posts"

    querystring = {
        "offset": f"{offset}",
        "max": "20",
        "dir": "fwd",
        "incl": "posts",
        "fp": "f_uo",
    }

    payload = ""

    headers = {
        # "cookie": "nlbi_2794913=Xw6tUoZ1Yn1ZCod+TDNW3QAAAABTuNqmO3y/Nl3Qre2XUveZ; __qca=P0-1182411913-1697632748159; _gcl_au=1.1.1948305308.1697632756; visid_incap_2794806=o3tnovQPSwaKdC2GYJf37dXRL2UAAAAAQUIPAAAAAADX/oeuz5dXpfRdUdrisGZR; nlbi_2794806=mfiTOgallxmWV5rJI5Ci3wAAAABFkz0uYDxMpzPynGTq+Nho; _ga=GA1.1.1026719266.1697632759; incap_ses_172_2794913=VazZE60rKGo9vzLHJBFjAhTmL2UAAAAAcdKI76Pha01rlKw7mb0T/A==; reese84=3:E+gr4n0YMC51H/3ujs1heQ==:olkdI8VvBdLkbB3beBkDu7fe6Bt5oBs14q26RJ8kHUREvw+6RHs1PBfmsjVNw4a/6NnrTjz1CwmMk0qH1C9ub3Hm6rrEIDAML0odN90tNiG3RepXwQ5SGAiuJbZY031PWyM7EMGmwTj7ruG4wiD4B6yKHqULssXEebwSSvuAx2rn/lv1MipgfJG+9T5782CSg3HNOeaqNZeZ/FILAkcGZflKjuG5dRJJ1C/SSzlNRbjte1SeRAqHnlkDBtKpHyTVJ+sab0F9s8O0dq87deBvzF7T5fQ89XLIDve9lokcuhCEk2gUefEqiEX88mG53lR/yyyyuaRnZMrj12C82k4aQ8avs2PAV7X4owu+MMgfgpkCFttweIRYgZ5y5fVE9z/ccB6ZSNgmIE1foWFVCOy4Wvwp8axL53Q0yo3wx0l1nvWbx0DDPUp/sNfN1R7mrUxDWJNwTM7oVkEcbEU0o9EfQttuPIVM/kBeq85EtY+BrVq0L4UxiaXuv6/pM84/m37m:E13e7JCFhLsSwg/9fksiXMwXur2WiBV8zyfemsNJQ28=; incap_ses_1635_2794806=sHCvbZl5TkLLErdJALCwFhTmL2UAAAAA/X+ck8LvGQBh+QQ7q3tHpg==; incap_ses_1290_2794913=niXyBmpEgku/D04qDAHnEQfoL2UAAAAAueJjxeBEGLz3j3+yB8AnhA==; visid_incap_2794913=460fJ5hORlKX/DPZQbGFriRaLmUAAAAAQkIPAAAAAACAVbuvAZ4+YtIpdwQcf9jCl9Yam27ZkCQU; nlbi_2794913_2147483392=MYRRdhSy2lRYJDOsTDNW3QAAAADnGPjud/wh3yfLUQEkv1Q3; incap_ses_676_2794913=oMMIIvbB3w9+gbjZfaNhCRXoL2UAAAAAa0bxqj5n7gp5sm6HC9+mBQ==; __gads=ID=d10423cbd4c287e8:T=1697632773:RT=1697638423:S=ALNI_MaSZmnacuX8LsTgFVinhqGHWCpUVg; __gpi=UID=00000c66da9eb251:T=1697632773:RT=1697638423:S=ALNI_MaE5RMf0UJ9muXolLKQS-OSvVaD6w; _ga_MH1FJK8TCY=GS1.1.1697638408.2.1.1697638471.59.0.0",
        # "authority": "api.gettr.com",
        # "accept": "application/json, text/plain, */*",
        # "accept-language": "en-US,en;q=0.9",
        # "lan": "en_us",
        # "origin": "https://gettr.com",
        # "referer": "https://gettr.com/",
        # "sec-ch-ua": "^\^Chromium^^;v=^\^118^^, ^\^Google",
        # "sec-ch-ua-mobile": "?0",
        # "sec-ch-ua-platform": "^\^Windows^^",
        # "sec-fetch-dest": "empty",
        # "sec-fetch-mode": "cors",
        # "sec-fetch-site": "same-site",
        "cookie": "visid_incap_2794806=N09vhMViQTaT9sYUQ55V4GvpL2UAAAAAQUIPAAAAAABaeCTkUTK4DvjCTVeMKuTe; nlbi_2794806=hwYYQpV3eQAj%2FAsYI5Ci3wAAAABp5uvsT8nW7%2FLKSSEQcGim; incap_ses_1636_2794806=R63pf9t%2FeGyWKhYgwD20FnB9QmUAAAAAe%2BAyHLZnQDBQatPqu3MMcg%3D%3D",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        # "ver": "2.7.0",
        # "x-app-auth": "^{^\^user^^: null, ^\^token^^: null^}",
    }

    # Request handling #################################################
    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring
    )

    return response


# Create list to store all user posts info
users_info = []
max_posts = 20

for user in [users[0]]:
    posts = []

    for offset in range(0, max_posts, 20):
        # JSON handling
        data = json.loads(get_response(user, offset).text)
        print(data)

        # Extract post ids
        num_posts = len(data["result"]["data"]["list"])
        post_ids = [
            data["result"]["data"]["list"][x]["activity"]["pstid"]
            for x in range(num_posts)
        ]

        for id in post_ids:
            posts_info = {}
            posts_info["post_id"] = id

            try:
                posts_info["text"] = data["result"]["aux"]["post"][id]["txt"]
            except KeyError:
                posts_info["text"] = "null"

            try:
                if "previmg" in data["result"]["aux"]["post"][id].keys():
                    posts_info["image"] = data["result"]["aux"]["post"][id]["previmg"]
                elif "imgs" in data["result"]["aux"]["post"][id].keys():
                    posts_info["image"] = (
                        "https://media.gettr.com/"
                        + data["result"]["aux"]["post"][id]["imgs"][0]
                    )
                else:
                    posts_info["image"] = "null"
            except KeyError:
                posts_info["image"] = "null"

            try:
                

            posts.append(posts_info)

        time.sleep(random.randint(2, 4))

    users_info.append(posts)
    print(f"Extracting info from user, {user}, done...")
    print(users_info)

# # Save data to csv
# df = pd.DataFrame(users_info, index=users)
# df.to_csv("gettr_data_test.csv")
