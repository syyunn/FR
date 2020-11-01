import requests
import pandas as pd
import io

search_term = "institution of investigations antidumping"


def replace_white_space_w_plus(text):
    fragments = text.split(" ")
    return "+".join(fragments)


search_term_url = replace_white_space_w_plus(search_term)
year = 1990
start = 2020
end = 2020
years = [i for i in range(start, end + 1)]

total = 0
for year in years:
    url = f"https://www.federalregister.gov/documents/search?conditions%5Bpublication_date%5D%5Byear%5D={year}&conditions%5Bterm%5D={search_term_url}&format=csv"
    content = requests.get(url).content
    df = pd.read_csv(io.StringIO(content.decode("utf-8")))

    cols = list(df.columns.values)

    df_investigation = pd.DataFrame(columns=cols)
    count = 0
    for index, row in df.iterrows():
        title = row["title"]
        abstract = row["abstract"]
        # if ": Antidumping Duty Orders" in title:  # or ': Antidumping and Countervailing Duty Orders' in title:
        if not isinstance(abstract, str):
            continue
        abstract = abstract.lower()
        if (
            "institution of" in abstract
            and "investigation" in abstract
            and ("antidumping" in abstract or "anti-dumping" in abstract)
        ):
            # print(title)
            title_split = title.split(';')
            try:
                product_countries = title_split[0].lower()
                product = product_countries.split('from')[0].strip()
                countries = product_countries.split('from')[1].strip()
                countries = countries.split(',')
                countries = countries[:-1] + countries[-1].split(' and')
                countries = [country.strip() for country in countries if len(country.strip()) > 0]
            except IndexError:
                product_countries = title_split[1].lower()
                product = product_countries.split('from')[0].strip()
                countries = product_countries.split('from')[1]
                countries = countries.split(',')
                countries = countries[:-1] + countries[-1].split(' and')
                countries = [country.strip() for country in countries if len(country.strip()) > 0]
            count += 1
            print(product, countries)
            df_investigation.loc[len(df_investigation)] = row
            pass
    print(year, count)
    total += count
print("total: ", total)
if __name__ == "__main__":
        pass
