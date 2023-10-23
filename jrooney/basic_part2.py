import httpx
from selectolax.parser import HTMLParser
import time


def get_html(base_url, page):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    response = httpx.get(base_url + str(page), headers=headers, follow_redirects=True)

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}. \nPage Limit Exceeded..."
        )
        return False
    html = HTMLParser(response.text)
    return html


def extract_text(html, selector):
    try:
        return html.css_first(selector).text()
    except AttributeError:
        return None


def parse_page(html):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    for product in products:
        item = {
            "name": extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
            "price": extract_text(product, "span[data-ui=sale-price]"),
            "savings": extract_text(product, "div[data-ui=savings-percent-variant2]"),
        }
        yield item


def main():
    url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="
    for x in range(1, 100):
        print(f"Gathering page: {x}")
        html = get_html(url, x)

        if html is False:
            break
        data = parse_page(html)
        for item in data:
            print(item)

        time.sleep(1)


if __name__ == "__main__":
    main()
