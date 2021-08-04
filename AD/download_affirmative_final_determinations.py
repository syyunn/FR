import requests
import pandas as pd
import io

search_term = "antidumping orders"


def replace_white_space_w_plus(text):
    fragments = text.split(" ")
    return "+".join(fragments)


search_term_url = replace_white_space_w_plus(search_term)
year = 1990
start = 1990
end = 2020
years = [i for i in range(start, end + 1)]

for year in years:
    print(year)
    url = f"https://www.federalregister.gov/documents/search?conditions%5Bpublication_date%5D%5Byear%5D={year}&conditions%5Bterm%5D={search_term_url}&format=csv"
    content = requests.get(url).content
    df = pd.read_csv(io.StringIO(content.decode("utf-8")))

    cols = list(df.columns.values)

    df_initial_levy = pd.DataFrame(columns=cols)
    count = 0
    for index, row in df.iterrows():
        title = row["title"]
        abstract = row["abstract"]
        # if ": Antidumping Duty Orders" in title:  # or ': Antidumping and Countervailing Duty Orders' in title:
        if not isinstance(abstract, str):
            continue
        if (
            "affirmative final determinations" in abstract
            and "is issuing" in abstract
            and "antidumping" in abstract
            and "order" in abstract
        ):
            print(abstract)
            count += 1
            pass
    print(year, count)
    # df.loc[len(df)] =
if __name__ == "__main__":
    pass
