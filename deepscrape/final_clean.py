import pandas as pd


"""for i in range(1, 22):
    df = pd.read_csv("clean_" + str(i) + ".csv")
    df = df.drop(["Unnamed: 0"], axis=1)
    df.to_csv("clean_" + str(i) + ".csv", index=False)"""
df = pd.read_csv("filev.csv")
df = df.drop([ "Unnamed: 0", "Unnamed: 0.1"], axis=1)
df.to_csv("clean_23.csv", index=False)