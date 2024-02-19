from bs4 import BeautifulSoup
from selenium import webdriver
import requests

def get_estate_data(url):
    driver = webdriver.Chrome()
    driver.get(url)
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

    return raw