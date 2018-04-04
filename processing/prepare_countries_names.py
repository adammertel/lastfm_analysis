import json
import copy

codes = json.load(open('./data/country_codes.json'))
countries = json.load(open('./data/ne_countries.geojson'))

ids_to_remove = []

for ci, country in enumerate(countries['features']):
    found = False
    for code in codes:
        if code['Code'] == country['properties']['ISO_A2']:
            found = True
            country['properties']['admin'] = code['Name']

    if found == False:
        country['properties']['admin'] = country['properties']['NAME']
        #ids_to_remove.append(ci)

#ids_to_remove.reverse()

#for id in ids_to_remove:
#del countries['features'][id]

with open('./data/countries_new.geojson', 'w') as file:
    json.dump(countries, file)