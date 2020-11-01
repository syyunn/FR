import requests
import pandas as pd
import io
import re

search_term = "institution of investigations antidumping"


def replace_white_space_w_plus(text):
    fragments = text.split(" ")
    return "+".join(fragments)


search_term_url = replace_white_space_w_plus(search_term)
year = 1990
start = 2012
end = 2020
years = sorted([i for i in range(start, end + 1)], reverse=True)

total = 0

cols = [
    "document_number",
    "publication_date",
    "product_name",
    "hs_codes",
    "countries",
    "html_url",
    "document_title",
]
df_investigation = pd.DataFrame(columns=cols)

for year in years:
    url = f"https://www.federalregister.gov/documents/search?conditions%5Bpublication_date%5D%5Byear%5D={year}&conditions%5Bterm%5D={search_term_url}&format=csv"
    content = requests.get(url).content
    df = pd.read_csv(io.StringIO(content.decode("utf-8")))

    # cols = list(df.columns.values)
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
            hs_codes = re.findall(r"[0-9]{4}\.[0-9]{2}\.[0-9]{2}", abstract)
            title_split = title.split(";")

            def _make_first_capital(text):
                return text[0].upper() + text[1:]

            def _parse_product_countries(index_for_product_countries):
                product_countries = title_split[index_for_product_countries].lower()
                product = product_countries.split("from")[0].strip()
                product = _make_first_capital(product)
                countries = product_countries.split("from")[1].strip()
                countries = countries.split(",")
                countries = countries[:-1] + countries[-1].split(" and")
                countries = [
                    _make_first_capital(country.strip())
                    for country in countries
                    if len(country.strip()) > 0
                ]
                return product, countries

            try:
                product, countries = _parse_product_countries(0)
            except IndexError:
                product, countries = _parse_product_countries(1)
            count += 1
            print(
                product,
                countries,
                hs_codes,
                row["html_url"],
                row["publication_date"],
                title,
                row["document_number"],
            )
            data = [
                row["document_number"],
                row["publication_date"],
                product,
                hs_codes,
                countries,
                row["html_url"],
                title,
            ]
            # print(cols)
            df_investigation.loc[len(df_investigation)] = data
            pass
    print(year, count)
    total += count
print("total: ", total)
df_investigation.to_csv(
    "./Investigation/FR_AD_Institution_of_Investigations.csv", index=False
)

if __name__ == "__main__":
    pass
