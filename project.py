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
    if len(columns) < len(table_cells):
        print(f"Warning: table has more columns than expected. Expected {len(columns)} columns, but found {len(table_cells)} \n")
        for i in range(len(columns)):
            row_data[columns[i]] = table_cells[i]
        for i in range(len(columns), len(table_cells)):
            row_data[f'Unknown Column {i}'] = table_cells[i]
    else:
        for i in range(len(table_cells)):
            row_data[columns[i]] = table_cells[i]
    return row_data

rows.pop(0)
for r in rows:
    australia_table.append(extract_row_data(columns, r))

# print(australia_table[0])

def clean_row_data(row: dict):
    for k in row.keys():
        val = row[k]
        if val.text.strip() == "":
            row[k] = "No data"
        links = val.find_all('a')
        for l in links:
            if l.get('title') is not None and '(page does not exist)' in l.get('title'):
                l.replace_with(l.text)
            if 'cite' in l.get('href'):
                l.parent.decompose()
        if k == 'Old-growth-extent' and row[k] != 'No data':
            data = row[k].text.strip()
            data = data.replace('\xa0', ' ')
            data = re.search('\d+(?:,\d{3})*(?:\.\d*)? (?:hectares|square kilometres|ha|acres)', data).group()

            parent = row[k].parent
            row[k].decompose()

            new_tag = soup.new_tag('td')
            new_tag.string = data
            parent.append(new_tag)

            row[k] = new_tag

    return row

# print(clean_row_data(australia_table[6]))

def prepare_table_data(columns, table):
    table_data = []

    rows = table.find_all('tr')
    rows.pop(0)

    for r in rows:
        r = extract_row_data(columns, r)
        r = clean_row_data(r)
        table_data.append(r)

    return table_data

def prepare_all_tables(columns, data):
    for k in data.keys():
        data[k] = prepare_table_data(columns, data[k])

    return data

data = prepare_all_tables(columns, data)
# print(len(data), '\n')
# print('FINAL DATA TEST: ', data['Europe'])

# print(data['Australia'][3]['Old-growth extent'].text, '\n')

# How many of the listed forests are in France?
europe = data['Europe']
france = [r for r in europe if 'France' in r['Country'].text]
print(len(france), '\n')

# How many of these forests are in the Tasmanian subregion?
australia = data['Australia']
tasmania = [r for r in australia if 'Tasmania' in r['Area'].text]
print(len(tasmania), '\n')

# Of those that has data in the Tasmanian list, what is the total land area?
tasmania_area_data = [r for r in tasmania if r['Old-growth extent'] != 'No data']
total = 0
for r in tasmania_area_data:
    area = r['Old-growth extent'].text
    area = area.replace(',', '')
    val = re.search('\d*', area).group()
    val = float(val)

    if 'square kilometres' in area:
        val *= 100
    total += val

print('Total area for Tasmanian forests: ',total, ' ha\n')
