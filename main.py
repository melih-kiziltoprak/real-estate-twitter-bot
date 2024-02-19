import credentials
import OpenAI_API
import Estate_Scraper
import Twitter_API

# For random real estate from uskudar:
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import random

random_page = random.randint(1, 100)
url = "https://www.hepsiemlak.com/uskudar?page=" + str(random_page)  

driver = webdriver.Chrome()
driver.get(url)
random_index = random.randint(0, 23)
driver.implicitly_wait(10)

xpath='/html/body/div[1]/div/div/div/div[2]/div/div/main/div[2]/div/div[1]/ul/li[2]/article/div/div[2]/div[1]/a'
link = driver.find_element("xpath", xpath)
link.click()

estate_ad_url = driver.current_url
"""

estate_ad_url = "https://www.hepsiemlak.com/istanbul-uskudar-murat-reis-satilik/daire/136218-371"

raw = Estate_Scraper.get_estate_data(estate_ad_url)
tweet_text = OpenAI_API.create_tweet_text(credentials.api_key, raw, estate_ad_url)
Twitter_API.send_tweet(tweet_text)
