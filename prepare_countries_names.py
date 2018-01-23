import json
import copy

codes = json.load(open('country_codes.json'))
countries = json.load(open('ne_countries.geojson'))

ids_to_remove = []

for ci, country in enumerate(countries['features']):
    found = False
    for code in codes:
        if code['Code'] == country['properties']['iso_a2']:
            found = True
            country['properties']['admin'] = code['Name']

    if found == False:
        ids_to_remove.append(ci)

ids_to_remove.reverse()

for id in ids_to_remove:
    del countries['features'][id]

with open('countries.geojson', 'w') as file:
    json.dump(countries, file)