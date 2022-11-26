import pandas

data = pandas.read_csv("aita_clean.csv")
for index, row in data.iterrows():
    print("*" * 100)
    print("ID")
    print(row["id"])
    print("TITLE")
    print(row["title"])
    print("BODY")
    print(row["body"])
    print()
    if index == 20:
        break