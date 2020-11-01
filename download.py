import requests
import pandas as pd
import io

search_term = "antidumping orders"


def replace_white_space_w_plus(text):
    fragments = text.split(' ')
    return "+".join(fragments)


search_term_url = replace_white_space_w_plus(search_term)
# url = f"https://www.federalregister.gov/documents/search?conditions%5Bterm%5D={search_term_url}&format=csv"
year = 2020

url = f"https://www.federalregister.gov/documents/search?conditions%5Bpublication_date%5D%5Byear%5D={year}&conditions%5Bterm%5D={search_term_url}&format=csv"
content = requests.get(url).content
df = pd.read_csv(io.StringIO(content.decode('utf-8')))

if __name__ == "__main__":
    pass
