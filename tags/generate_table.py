import json
import csv
import io

import sys
reload(sys)
sys.setdefaultencoding('utf8')

countries_tags = json.load(io.open('countries_tags.json', encoding='utf-8'))
countries_not_found = json.load(
    io.open('countries_not_found.json', encoding='utf-8'))
tags_dict = json.load(io.open('tags_list.json', encoding='utf-8'))

# tags list
tags_list = []
for tag in tags_dict:
    tags_dict[tag]['id'] = tag
    tags_list.append(tags_dict[tag])

s_tags_list = sorted(tags_list, key=lambda k: -1 * k['val'])
#print(s_tags_list)

# headers
header1 = ['tag key']
for tag in s_tags_list:
    header1.append(tag['id'])

header2 = ['tag name']
for tag in s_tags_list:
    header2.append(str(tag['name']))

header3 = ['tag sum']
for tag in s_tags_list:
    header3.append(str(tag['val']))

countries_rows = []
# countries
for country in countries_tags:
    if country not in countries_not_found and len(
            countries_tags[country].keys()):
        country_row = [country] + [0] * (len(header2) - 1)

        for tag in countries_tags[country]:
            val = countries_tags[country][tag]

            for si, s_tag in enumerate(s_tags_list):
                if s_tag['id'] == tag:
                    country_row[si + 1] = val
                    break

        countries_rows.append(country_row)

with io.open('./outputs/tags_table.csv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t', lineterminator='\n')

    writer.writerow(header1)
    writer.writerow(header2)
    writer.writerow(header3)

    for country_row in countries_rows:
        writer.writerow(country_row)
