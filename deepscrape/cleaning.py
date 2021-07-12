import pandas as pd



df = pd.read_csv("finaly.csv")
print(len(df))
df.dropna(subset = ["size"], inplace=True)
df = df.drop_duplicates(subset=['URL'])
print(len(df))
df.to_csv("clean.csv")