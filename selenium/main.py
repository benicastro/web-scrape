#############################################################
# Gab Data Extraction using Selenium                  #######
# by Benedict Z. Castro | benedict.zcastro@gmail.com  #######
#############################################################

# Import needed modules/libraries ###########################
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selectolax.parser import HTMLParser

# Keep Chrome browser open after program finishes ###########
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create driver with Chrome #################################
driver = webdriver.Chrome(options=chrome_options)
# For maximizing window
driver.maximize_window()
# Gives an implicit wait for 20 seconds
driver.implicitly_wait(20)

# Main - Extract the information needed #####################


def main():
    url = "https://4chansearch.com/?q=DallE+more%3Apol&s=1"

    for page in range(2, 3):
        driver.get(url)
        page_element = driver.find_element(
            By.CSS_SELECTOR, value=f"div.gsc-cursor-page[aria-label='Page {page}']"
        )
        page_element.click()
        time.sleep(3)
        page_source = driver.page_source
        driver.close()
        html = HTMLParser(page_source)
        print(html.html)

    # # Loop through all users
    # for user in users_list:
    #     # Request user data from website
    #     driver.get(base_url + user)
    #     # Let the browser scroll to the end of the page
    #     for i in range(3):
    #         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #         time.sleep(4)

    #     # Create a dictionary to contain all information
    #     info = {}

    #     info["user_name"] = driver.find_element(
    #         By.CSS_SELECTOR,
    #         value=f'strong.{"_3_54N _1-fAn _317eq mVHNg _2ZzNB _3XmA1 _1kAFo Y32gl".replace(" ", ".")}',
    #     ).text

    #     info["date_joined"] = driver.find_element(
    #         By.CSS_SELECTOR,
    #         value=f'span.{"_33mR1 _UuSG _3_54N a8-QN _2cSLK L4pn5 RiX17".replace(" ", ".")}',
    #     ).text[13:]

    #     info["user_image"] = driver.find_element(
    #         By.CSS_SELECTOR,
    #         value=f'div.{"_UuSG _3mBt0 _1FVXP _1lNuM _2I3eh".replace(" ", ".")} > img',
    #     ).get_attribute("src")

    #     info["cover_photo"] = driver.find_element(
    #         By.CSS_SELECTOR,
    #         value=f'img.{"Os0yf _UuSG _3ejos ALevz".replace(" ", ".")}',
    #     ).get_attribute("src")

    #     info["about"] = driver.find_element(
    #         By.CSS_SELECTOR,
    #         value="div._9utbn",
    #     ).text

    #     # Elements with same class name for the number of gabs and followers/following
    #     flw_elem = driver.find_elements(
    #         By.CLASS_NAME,
    #         value="_UuSG ALevz _3Ujf8 _1o5Ge _81_1w _1E64f _3ddB-".replace(" ", "."),
    #     )
    #     info["num_gabs"] = flw_elem[0].get_attribute("title")[:-5]
    #     info["num_followers"] = flw_elem[1].get_attribute("title")[:-10]
    #     info["num_following"] = flw_elem[2].get_attribute("title")[:-10]

    #     # Declare the number of posts to be scraped
    #     posts_target_count = 50
    #     posts_info = []

    #     # Get all elements that contain posts
    #     try:
    #         post_elem = driver.find_elements(
    #             By.CSS_SELECTOR,
    #             value=f"div.{'_UuSG _2I3eh _33UDc fArsv _3pxdP _1qzTN _12x1x pwK6B'.replace(' ', '.')}",
    #         )

    #         for elem in post_elem:
    #             # Post ID link
    #             post_id = elem.find_element(
    #                 By.CSS_SELECTOR,
    #                 value=f"div > div > div > div.{'_UuSG _36P3u _2kzXy SslQJ _1unCp'.replace(' ', '.')} > div a.{'_UuSG _3Ujf8 yigUm ALevz _1XpDY _81_1w _1o5Ge A0UHB'.replace(' ', '.')}",
    #             ).get_attribute("href")

    #             # Post text
    #             try:
    #                 post_text = elem.find_element(
    #                     By.CSS_SELECTOR,
    #                     value=f"div > div > div div._1FwZr._81_1w",
    #                 ).text
    #             except:
    #                 post_text = "no text"

    #             # Post media
    #             try:
    #                 post_media = elem.find_element(
    #                     By.CSS_SELECTOR,
    #                     value=f"div > div > div div.{'_UuSG _3QyQz _2z1u_ _1qzTN _3dx6D _12x1x'.replace(' ', '.')} div.react-photo-gallery--gallery img",
    #                 ).get_attribute("src")
    #             except:
    #                 post_media = "no media"

    #             # Post reacts
    #             try:
    #                 post_reacts = elem.find_element(
    #                     By.CSS_SELECTOR,
    #                     value=f"div > div > div span.{'_3u7ZG _UuSG _3_54N a8-QN _2cSLK L4pn5 RiX17'.replace(' ', '.')}",
    #                 ).text
    #                 if "k" in post_reacts:
    #                     post_reacts = float(post_reacts[:-1]) * 1000
    #                 else:
    #                     post_reacts = int(post_reacts)
    #             except:
    #                 post_reacts = 0

    #             # Post replies
    #             try:
    #                 post_replies = elem.find_element(
    #                     By.CSS_SELECTOR,
    #                     value=f"div > div > div a.{'_UuSG _3_54N L4pn5 _3Ujf8 _1o5Ge _81_1w _3TwRa _3OtSI ALevz A0UHB'.replace(' ', '.')}",
    #                 ).text
    #                 if "k" in post_replies:
    #                     post_replies = float(post_replies.split()[0][:-1]) * 1000
    #                 else:
    #                     post_replies = int(post_replies.split()[0])
    #             except:
    #                 post_replies = 0

    #             # Post reposts
    #             try:
    #                 post_reposts = elem.find_element(
    #                     By.CSS_SELECTOR,
    #                     value=f"div > div > div button.{'_UuSG _3_54N L4pn5 _3Ujf8 _1o5Ge _81_1w _3TwRa _3OtSI ALevz A0UHB'.replace(' ', '.')}",
    #                 ).text
    #                 if "k" in post_reposts:
    #                     post_reposts = float(post_reposts.split()[0][:-1]) * 1000
    #                 else:
    #                     post_reposts = int(post_reposts.split()[0])
    #             except:
    #                 post_reposts = 0

    #             # Post quotes
    #             try:
    #                 post_quotes = elem.find_element(
    #                     By.CSS_SELECTOR,
    #                     value=f"div > div > div button:nth-child(4)",
    #                 ).text
    #                 if "k" in post_quotes:
    #                     post_quotes = float(post_quotes.split()[0][:-1]) * 1000
    #                 else:
    #                     post_quotes = int(post_quotes.split()[0])
    #             except:
    #                 post_quotes = 0
    #             post = {
    #                 "post_id": post_id,
    #                 "post_text": post_text,
    #                 "post_media": post_media,
    #                 "post_reacts": post_reacts,
    #                 "post_replies": post_replies,
    #                 "post_reposts": post_reposts,
    #                 "post_quotes": post_quotes,
    #                 "engagement_count": post_reacts
    #                 + post_reposts
    #                 + post_replies
    #                 + post_quotes,
    #             }
    #             posts_info.append(post)
    #             if posts_target_count == len(posts_info):
    #                 break

    #         info["last_posts"] = posts_info

    #     except:
    #         info["last_posts"] = "None"

    #     # Compute for average engagement
    #     num_last_posts = len(posts_info)
    #     total_engagement = 0

    #     for i in range(num_last_posts):
    #         total_engagement += posts_info[i]["engagement_count"]

    #     info["avg_engagement"] = total_engagement / num_last_posts

    #     users_info.append(info)

    # # Close the browser
    # driver.quit()

    # print(users_info)

    # # Save data to csv
    # df = pd.DataFrame(users_info)
    # df.to_csv("gab_data.csv")


# Run the program
if __name__ == "__main__":
    main()
