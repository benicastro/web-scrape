# user_agent = 'Mozilla/5.0 (Linux; Android 11; 100011886A Build/RP1A.200720.011) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.69 Safari/537.36'
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
sec_ch_ua = '"Google Chrome";v="104", " Not;A Brand";v="105", "Chromium";v="104"'
referer = "https://www.google.com"


def interceptor(request):
    # delete the "User-Agent" header and
    # set a new one
    del request.headers["user-agent"]  # Delete the header first
    request.headers["user-agent"] = user_agent
    # set the "Sec-CH-UA" header
    request.headers["sec-ch-ua"] = sec_ch_ua
    # set the "referer" header
    request.headers["referer"] = referer


def get_html_selenium(url, **kwargs):
    """This function returns the HTML content of a given website url and page number using selenium."""
    # Configure browser
    s = Service("/tmp/chrome/latest/chromedriver_linux64/chromedriver")
    options = webdriver.ChromeOptions()
    options.binary_location = "/tmp/chrome/latest/chrome-linux/chrome"

    options.add_argument("--headless=new")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=8888")
    options.add_argument("--homedir=/tmp/chrome/chrome-user-data-dir")
    options.add_argument("--user-data-dir=/tmp/chrome/chrome-user-data-dir")
    PROXY = get_oxylabs_proxy()["https"]
    # options.add_argument('--proxy-server=%s' % PROXY)

    selenium_wire_options = {
        "proxy": {
            "http": PROXY,
            "verify_ssl": False,
        },
    }

    prefs = {
        "download.default_directory": "/tmp/chrome/chrome-user-data-di",
        "download.prompt_for_download": False,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        service=s, options=options, seleniumwire_options=selenium_wire_options
    )
    driver.request_interceptor = interceptor
    time.sleep(5)
    driver.get(url)

    # Navigate through pages
    if kwargs.get("page") and kwargs.get("page") >= 2:
        page_number = str(kwargs.get("page"))
        page_element = driver.find_element(
            By.CSS_SELECTOR,
            value=f"div.gsc-cursor-page[aria-label='Page {page_number}']",
        )
        page_element.click()
        time.sleep(5)
        page_source = driver.page_source
    else:
        page_source = driver.page_source
    driver.close()

    html = HTMLParser(page_source)
    # print(html.html)
    return html


def get_html(url, **kwargs):
    """This function returns the HTML content of a given website url using httpx."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
    }

    if kwargs.get("page"):
        response = httpx.get(
            url + "/" + str(kwargs.get("page")), headers=headers, follow_redirects=True
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
