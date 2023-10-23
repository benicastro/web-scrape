import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin
from dataclasses import dataclass, asdict


@dataclass
class Item:
    name: str | None
    item_num: str | None
    price: str | None
    rating: float | None


def get_html(url, **kwargs):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    if kwargs.get("page"):
        response = httpx.get(
            url + str(kwargs.get("page")), headers=headers, follow_redirects=True
        )
    else:
        response = httpx.get(url, headers=headers, follow_redirects=True)

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


def parse_search_page(html):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")
    for product in products:
        yield urljoin("https://www.rei.com", product.css_first("a").attributes["href"])


def parse_item_page(html):
    new_item = Item(
        name=extract_text(html, "h1#product-page-title"),
        item_num=extract_text(html, "span#product-item-number"),
        price=extract_text(html, "span#buy-box-product-price"),
        rating=extract_text(html, "span.cdr-rating__number_13-5-3"),
    )
    return new_item


def main():
    products = []
    base_url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="

    for x in range(1, 2):
        print(f"Gathering page: {x}")

        html = get_html(base_url, page=x)

        if html is False:
            break

        product_urls = parse_search_page(html)

        for url in product_urls:
            print(url)
            html = get_html(url)
            products.append(parse_item_page(html))
            time.sleep(1)
        for product in products:
            print(asdict(product))


if __name__ == "__main__":
    main()
