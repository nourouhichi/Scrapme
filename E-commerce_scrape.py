from selenium import webdriver
from bs4 import BeautifulSoup as bs
from requests import get
import pandas as pd
from time import sleep


driver = webdriver.Chrome()
driver.get("https://www.vapeshop.co.uk")
prod_name, prod_price, prod_decr, prod_img, avai =[], [], [], [], []
#google what is my useragent to fill the useragent field
headers = {
    'User-Agent': "",
}
try:
    while(driver.find_element_by_class_name("btn.porto-load-more.porto-products-load-more.load-on-click")):
        driver.find_element_by_class_name("btn.porto-load-more.porto-products-load-more.load-on-click").click()
        sleep(1)
except Exception:
    content = driver.page_source
    soup = bs(content, features="lxml")
    items = soup.find_all('a', class_="product-loop-title")
    for item in range(len(items)):
        r = get("https://www.vapeshop.co.uk" + str(items[item]["href"]))
        soup_ = bs(r.content, features="lxml")
        name = soup_.find_all('div', class_="product-name top-product-detail", limit=1)
        prod_name.append(name[0].text)
        price = soup_.find_all('span', class_="money", limit=1)
        prod_price.append(price[0].text)
        description = soup_.find_all("div", class_="product-tabs-content-inner clearfix", limit=1)
        prod_decr.append(description[0].text)
        stock = soup_.find_all('span', class_="in-stock", limit=1)
        avai.append(stock[0].text)
        img = soup_.find_all("img")
        for image in img:
            if image.has_attr('id'):
                if image['id'] == "product-featured-image":
                    prod_img.append(image["data-src"])
                    break
d = {'name': prod_name, 'price': prod_price, 'description': prod_decr, 'image': prod_img, 'availability': avai}
df = pd.DataFrame(data=d)
