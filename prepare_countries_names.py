import json

codes = json.load(open('country_codes.json'))
countries = json.load(open('ne_countries.geojson'))

for country in countries['features']:
    country_name = 'not found'
    for code in codes:
        if code['Code'] == country['properties']['iso_a2']:
            country_name = code['Name']
    country['properties']['admin'] = country_name

with open('countries.geojson', 'w') as file:
    json.dump(countries, file)