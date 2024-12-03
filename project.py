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

print(html)