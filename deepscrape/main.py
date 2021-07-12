from selenium import webdriver
from bs4 import BeautifulSoup as bs
from requests import get, session
import pandas as pd
from PIL import Image
from io import BytesIO
import urllib3

urllib3.disable_warnings()
src, a, src_ , sub_a, content_type, size, url ,name_arr, uid_arr, id_arr, n_arr, listy = [], [], [], [], [], [], [], [], [], [], [], []
count = 0
#cleaning df
df = pd.read_csv("export_opendata_lrk SCRAPE.csv") 
nan_value = float("NaN")
df.replace("", nan_value, inplace=True)
df.dropna(subset = ["URL"], inplace=True)
df = df.drop_duplicates(subset=['URL'])
df['URL'].astype(str)
for i in df['URL']:
    if i.split('.')[0] != "http://www" and i.split('.')[0] != "https://www":
        listy.append(i)
for x in listy:
    index_names = df[ df['URL'] == x ].index
    df.drop(index_names, inplace = True)
print(df)
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.208",
}
"""df.to_csv("auxi.csv")"""
df = pd.read_csv("filev.csv") 
for id in df.UID:
    id_arr.append(int(id))
for n in df.Type:
    n_arr.append(str(n))
for link in df.URL:
    print(count)
    uid = id_arr[count]
    name = n_arr[count]
    count += 1
    r = get(link, headers=headers, verify=False)
    soup = bs(r.content, features="lxml")
    img = soup.find_all('img')
    href = soup.find_all('a')
    a = []
    for i in img:
        try: 
            if i.has_attr('src'):
                x = get(i['src'])
                img_data = x.content    
                ima = Image.open(BytesIO(img_data))
                content_type.append(ima.format)
                size.append(int(ima.height) * int(ima.width))
                src_.append(i["src"])
                name_arr.append(name)
                uid_arr.append(uid)
        except Exception:
            pass
    for x in href:
        if x.has_attr('href'):
            a.append(x["href"])
    if a is not []:
        for y in a:
            if link in str(y) and len(y) > len(link):
                r = get(str(y), headers=headers, verify=False)
                soup = bs(r.content, features="lxml")
                img = soup.find_all('img')
                for i in img:
                    if i.has_attr('src') and i["src"] not in src_:
                        try:
                            img_data = get(i["src"]).content    
                            ima = Image.open(BytesIO(img_data))
                            content_type.append(ima.format)
                            size.append(int(ima.height) * int(ima.width))
                            src_.append(i["src"])
                            name_arr.append(name)
                            uid_arr.append(uid)
                        except Exception:
                            pass
            elif len(str(y)) > 1:
                if str(y)[0] == '/':
                    try:
                        r = get(link + str(y), headers=headers, verify=False)
                        soup = bs(r.content, features="lxml")
                        img = soup.find_all('img')
                        for i in img:
                            if str(i["src"])[0] == "/":
                                im = link + str(i["src"])
                                try:
                                    if im not in src_:
                                        img_data = get(im).content    
                                        ima = Image.open(BytesIO(img_data))
                                        content_type.append(ima.format)
                                        size.append(int(ima.height) * int(ima.width))
                                        src_.append(im)
                                        name_arr.append(name)
                                        uid_arr.append(uid)
                                except Exception:
                                    pass
                            else:
                                im = i["src"]
                                try:
                                    if im not in src_:
                                        img_data = get(im).content    
                                        ima = Image.open(BytesIO(img_data))
                                        content_type.append(ima.format)
                                        size.append(int(ima.height) * int(ima.width))
                                        src_.append(im)
                                        name_arr.append(name)
                                        uid_arr.append(uid)
                                except Exception:
                                    pass
                    except Exception:
                        pass
save = pd.DataFrame(uid, name_arr,src_)
df_ = pd.DataFrame({"UID":uid_arr, "name":name_arr, "URL": src_, "Type": content_type, "size": size})
df_.to_csv("finaly.csv")