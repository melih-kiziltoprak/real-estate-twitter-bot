from selenium import webdriver
from bs4 import BeautifulSoup
from openai import OpenAI
import tweepy
from tweepy import API
import requests
import random

import credentials

# Getting raw data from hepsiemlak
#url = "https://www.hepsiemlak.com/istanbul-uskudar-sultantepe-satilik/daire/141821-25"  


random_page = random.randint(1, 100)
url = "https://www.hepsiemlak.com/uskudar?page=" + str(random_page)  

driver = webdriver.Chrome()
driver.get(url)
random_index = random.randint(0, 23)
driver.implicitly_wait(10)

xpath='/html/body/div[1]/div/div/div/div[2]/div/div/main/div[2]/div/div[1]/ul/li[2]/article/div/div[2]/div[1]/a'
link = driver.find_element("xpath", xpath)
link.click()


tweet_url = driver.current_url
xpath = '/html/body/div[1]/div/div/div/section[3]/div/div[1]/div[1]/section[1]/div[1]/div[3]/p'
price = ""
try:
    price = driver.find_element("xpath", xpath).text
except:
    print("COULD NOT FIND PRICE IN: " + tweet_url)

#p = input("o")

xpath = '//*/div/div[1]/div[1]/section[1]/div[4]/div'

html_content = driver.find_element("xpath", xpath).get_attribute("outerHTML")

soup = BeautifulSoup(html_content, 'html.parser')
li_elements = soup.select('.adv-info-list li')
ilan_bilgileri = {}
for li in li_elements:
    spans = li.find_all('span')
    if len(spans) >= 2:
        key = spans[0].get_text(strip=True)
        value = spans[1].get_text(strip=True)
        ilan_bilgileri[key] = value

xpath = '//*/div/div[1]/div[1]/section[3]/section[1]/section/div'
driver.implicitly_wait(10)
html_content = driver.find_element("xpath", xpath).get_attribute("outerHTML")

soup = BeautifulSoup(html_content, 'html.parser')
aciklama = ""
try:
    aciklama = soup.find('p').get_text(strip=True)
    print("found aciklama")
    #o = input("exit??")
except:
    print("couldnt find aciklma in " + tweet_url)
    o = input("exit??")
raw = price + "\n\n" + str(ilan_bilgileri) +  "\n\n" + aciklama
print(raw)


#c = input("continue or interrupt")

# Image

for photo_index in range(1, 5):
    xpath = '/html/body/div[1]/div/div/div/section[2]/div/div/div/div/div/div[2]/div[1]/div[' + str(photo_index) +']/img'

    img_element = driver.find_element("xpath", xpath)
    img_src = img_element.get_attribute('src')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = requests.get(img_src, headers=headers)
    print(response.status_code)
    img_filename = 'downloaded_image_' +str(photo_index)+ '.jpg'
    with open(img_filename, 'wb') as img_file:
        img_file.write(response.content)
    tweet_url = driver.current_url
    
driver.quit()

# OpenAI API
prompt_text = "aşağıdaki bilgilerle Emlak Öneri hesabım ilgi çekici bir twitter post'u hazırla, Yatırım fırsatı olarak değerlendir. 800 karakteri kesinlikle aşmasın! Emoji kullan!:\n" + raw 
client = OpenAI(api_key = credentials.api_key)
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt_text,
        }
    ],
    model="gpt-3.5-turbo",
)

"""
post_length = 275 - len(tweet_url)
tweet_text = response.choices[0].message.content
print(tweet_text)
tweet_text = tweet_text[:post_length] + "... " + tweet_url
"""
tweet_text = response.choices[0].message.content + "   " + tweet_url




def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""
    auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""
    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    return client

client_v1 = get_twitter_conn_v1(credentials.consumer_key, credentials.consumer_secret, credentials.access_token, credentials.access_token_secret)
client_v2 = get_twitter_conn_v2(credentials.consumer_key, credentials.consumer_secret, credentials.access_token, credentials.access_token_secret)

photos = []
for photo_index in range(1, 5):
    media = client_v1.media_upload(filename= ("downloaded_image_" + str(photo_index) + ".jpg") )
    photos.append(media.media_id)

tweet_response = client_v2.create_tweet(text=tweet_text[:250], media_ids=photos)
print(tweet_response)
tweet_id = tweet_response.data['id']
for i in range(1, int(len(tweet_text) / 250) + 1):
    reply_text = tweet_text[i*250 : (i+1)*250]
    if(i != int(len(tweet_text) / 250)):
        reply_text += " +++++"
    tweet_id = client_v2.create_tweet(
        text=reply_text,
        in_reply_to_tweet_id=tweet_id
    ).data['id']
