import pandas as pd
from requests import get
import urllib3

urllib3.disable_warnings()
listy = []
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
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.208",
}
print(df)
for i in df['URL']:
    try:
        r = get(str(i), headers=headers, verify=False)
        print("yes")
    except Exception:
        index_names = df[ df['URL'] == i ].index
        df.drop(index_names, inplace = True)
        print("ok")
    print(len(df))
print(df)
df.to_csv("auxi.csv")