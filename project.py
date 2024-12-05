from bs4 import BeautifulSoup
import requests
import re
import os

print(' ')

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

for t in tables:
    heading = None
    for elem in t.find_all_previous(['h2', 'h3']):
        if elem.parent.get('class')!= ['mw-parser-output']:
            heading = elem.text
            break
    #print(heading)
    data[heading] = t

# print('\n', data['Australia'])

table = data['Australia']
first_row = table.tr
# for td in first_row:
#     print(td.text)

columns = []
for td in first_row:
    if td.text.strip() != '':
        columns.append(td.text.strip())
# print(columns)

rows = table.find_all('tr')
# print(rows[1])

example_row = rows[1]
table_cells = example_row.find_all('td')
# print(table_cells)

row_data = {}
for i in range(len(table_cells)):
    row_data[columns[i]] = table_cells[i]

# print(row_data['Country'])
# print(row_data['Old-growth forest type'])

australia_table = []

def extract_row_data(columns, row):
    row_data = {}
    table_cells = row.find_all('td')
    for i in range(len(table_cells)):
        row_data[columns[i]] = table_cells[i]

    return row_data

rows.pop(0)
for r in rows:
    australia_table.append(extract_row_data(columns, r))

print(australia_table[0])