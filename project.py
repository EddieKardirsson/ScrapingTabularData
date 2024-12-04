from bs4 import BeautifulSoup
import requests
import re
import os


def get_html(url, path):
    response = requests.get(url)
    with open(path, 'w', encoding='utf--8') as f:
        f.write(response.text)


url = "https://en.wikipedia.org/wiki/List_of_old-growth_forests"
path = "./html_docs/old_growth_forests.html"

if not os.path.exists(path):
    get_html(url, path)

with open(path, 'r', encoding='utf8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

tables = soup.find_all('table', attrs={'class': 'wikitable sortable'})

data = {}
# for t in tables:
#     heading_div = t.find_previous_sibling(['div', {'class': 'mw-heading'}])
#     heading = heading_div.find(['h2', 'h3'])
#     print(heading)

for t in tables:
    heading = None
    for elem in t.find_all_previous(['h2', 'h3']):
        if elem.parent.get('class')!= ['mw-parser-output']:
            heading = elem.text
            break
    print(heading)
    data[heading] = t

print('\n', data['Australia'])