# import json
# import requests

# file_path = "C:\\Users\\bened\\Downloads\\benz.jpg"
# search_url = "https://yandex.com/images/search"
# files = {"upfile": ("benz", open(file_path, "rb"), "image/jpeg")}
# params = {
#     # "tmpl_version": "releases/frontend/images/v1.1177.0#24640fb79140881cd203ed5abccc106754f23004",
#     "rpt": "imageview",
#     "format": "json",
#     # "request": '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}',
#     # "request": '{"blocks":[{"block":"extra-content"}]}',
#     "request": '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}',
#     # "request": '{"blocks":[{"block":"block":"i-react-ajax-adapter:ajax"}]}',
# }
# response = requests.post(search_url, params=params, files=files)
# query_string = json.loads(response.content)["blocks"][0]["params"]["url"]
# img_search_url = search_url + "?" + query_string
# print(img_search_url)
# print(response.content)

urls = [
    "s3://activefence-user/ilank/gen-ai/media/55220e9aecbecab1f4b56a9d1880485784b19c6eb0e9e42a6eda53d5787eb316"
]

bucket = urls[0].split("/")[2]
print(bucket)

key = urls[0].split(f"{bucket}/")[1]
print(key)
################################################################################################################################


# def yandex_query():
#     # cookies = {
#     #     "is_gdpr": "0",
#     #     "i": "+ypzlkm9Hr0MBih5oTcatnx9NYZNHz5aP4e46b6BX0YwYxhFCcEex2/l9Dm3wYGlTa0WfvfFzTGcUInHfNTDx66uMas=",
#     #     "yandexuid": "7046405321699539092",
#     #     "yashr": "2612848891699539092",
#     #     "gdpr": "0",
#     #     "_ym_uid": "1699539095809496478",
#     #     "_ym_isad": "2",
#     #     "bh": "EkEiR29vZ2xlIENocm9tZSI7dj0iMTE5IiwgIkNocm9taXVtIjt2PSIxMTkiLCAiTm90P0FfQnJhbmQiO3Y9IjI0IhoFIng4NiIiECIxMTkuMC42MDQ1LjEyNCIqAj8wMgIiIjoJIldpbmRvd3MiQggiMTQuMC4wIkoEIjY0IlJdIkdvb2dsZSBDaHJvbWUiO3Y9IjExOS4wLjYwNDUuMTI0IiwgIkNocm9taXVtIjt2PSIxMTkuMC42MDQ1LjEyNCIsICJOb3Q/QV9CcmFuZCI7dj0iMjQuMC4wLjAiWgI/MA==",
#     #     "yandex_gid": "116114",
#     #     "is_gdpr_b": "CK2pbRDz2AEoAg==",
#     #     "_yasc": "ZqHA/3Pogwq4ms7k4buC3GbCZTaCBppUJxDiprhAS0DIxv/xS1di0XWdLl7qEupaRq9s+tj+Z6iQEg==",
#     #     "yuidss": "7046405321699539092",
#     #     "ymex": "2014906369.yrts.1699546369",
#     #     "bh": "Ej8iR29vZ2xlIENocm9tZSI7dj0iMTE5IiwiQ2hyb21pdW0iO3Y9IjExOSIsIk5vdD9BX0JyYW5kIjt2PSIyNCIaBSJ4ODYiIhAiMTE5LjAuNjA0NS4xMjQiKgI/MDoJIldpbmRvd3MiQggiMTQuMC4wIkoEIjY0IlJcIkdvb2dsZSBDaHJvbWUiO3Y9IjExOS4wLjYwNDUuMTI0IiwiQ2hyb21pdW0iO3Y9IjExOS4wLjYwNDUuMTI0IiwiTm90P0FfQnJhbmQiO3Y9IjI0LjAuMC4wIiI=",
#     #     "cycada": "+oAyhgir1zpxEfeoYb4/F4C7V7g6cmRlW7oOz6u5hYY=",
#     #     "yp": "4294967295.skin.s#1715317152.szm.1_5:1280x720:725x563#1702138368.ygu.1",
#     #     "my": "YwA=",
#     #     "_ym_d": "1699549152",
#     # }

#     headers = {
#         # "authority": "yandex.com",
#         # "accept": "application/json, text/javascript, */*; q=0.01",
#         # "accept-language": "en-US,en;q=0.9,he-IL;q=0.8,he;q=0.7",
#         # "device-memory": "8",
#         # "downlink": "8.2",
#         # "dpr": "1.5",
#         # "ect": "4g",
#         # "referer": f"https://yandex.com/images/search?text={kw}",
#         # "rtt": "50",
#         # "sec-ch-ua": '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
#         # "sec-ch-ua-arch": '"x86"',
#         # "sec-ch-ua-bitness": '"64"',
#         # "sec-ch-ua-full-version": '"119.0.6045.124"',
#         # "sec-ch-ua-full-version-list": '"Google Chrome";v="119.0.6045.124", "Chromium";v="119.0.6045.124", "Not?A_Brand";v="24.0.0.0"',
#         # "sec-ch-ua-mobile": "?0",
#         # "sec-ch-ua-model": '""',
#         # "sec-ch-ua-platform": '"Windows"',
#         # "sec-ch-ua-platform-version": '"14.0.0"',
#         # "sec-ch-ua-wow64": "?0",
#         # "sec-fetch-dest": "empty",
#         # "sec-fetch-mode": "cors",
#         # "sec-fetch-site": "same-origin",
#         "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
#         # "viewport-width": "725",
#         # "x-requested-with": "XMLHttpRequest",
#     }

#     response = requests.get(
#         f"https://yandex.com/images/search?tmpl_version=releases%2Ffrontend%2Fimages%2Fv1.1177.0%2324640fb79140881cd203ed5abccc106754f23004&
#         format=json&
#         request=%7B%22blocks%22%3A%5B%7B%22block%22%3A%22extra-content%22%2C%22params%22%3A%7B%7D%2C%22version%22%3A2%7D%2C%7B%22block%22%3A%7B%22block%22%3A%22i-react-ajax-adapter%3Aajax%22%7D%2C%22params%22%3A%7B%22type%22%3A%22ImagesApp%22%2C%22ajaxKey%22%3A%22serpList%2Ffetch%22%7D%2C%22version%22%3A2%7D%5D%2C%22metadata%22%3A%7B%22bundles%22%3A%7B%22lb%22%3A%22zq%7BO7D)vxy%2B(((ek%2BNw%7D%22%7D%2C%22assets%22%3A%7B%22las%22%3A%22justifier-height%3D1%3Bjustifier-setheight%3D1%3Bfitimages-height%3D1%3Bjustifier-fitincuts%3D1%3Breact-with-dom%3D1%3B3c52cf.0%3D1%3B239.0%3D1%3B215.0%3D1%3Ba2d3bd.0%3D1%3Bd0371f.0%3D1%3B135.0%3D1%3B763201.0%3D1%3B199.0%3D1%3B207.0%3D1%3B319.0%3D1%3Bd8337b.0%3D1%3Bd031f2.0%3D1%3B16966d.0%3D1%22%7D%2C%22extraContent%22%3A%7B%22names%22%3A%5B%22i-react-ajax-adapter%22%5D%7D%7D%7D&
#         yu=7046405321699539092&
#         lr=116114&
#         p=1&
#         rpt=image&
#         serpListType=horizontal&
#         serpid=K4NrIAn1GJGA65w5K8wlKg&
#         text={kw}&
#         uinfo=sw-1280-sh-720-ww-725-wh-563-pd-1.5-wp-16x9_1920x1080",
#         headers=headers,
#     )

#     data = response.json()
#     return data


# print(yandex_query())
