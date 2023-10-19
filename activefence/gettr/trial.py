import httpx
from selectolax.parser import HTMLParser

url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals"
# url = "https://gettr.com/user/valiantnews"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
}

response = httpx.get(url, headers=headers)
html = HTMLParser(response.text)


def extract_text(html, selector):
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None


products = html.css("li.VcGDfKKy_dvNbxUqm29K")

for product in products:
    item = {
        "name": extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
        "price": extract_text(product, "span[data-ui=sale-price]"),
    }

    print(item)
