from base import *

filepath_import = './data/countries_import.json'
filepath_countries_topartists = './data/countries_topartists1000.json'
filepath_origin = './data/artists_origin.csv'

countries = json.load(open(filepath_countries_topartists))

countries_no = len(countries)
processed_no = 0

clean_json(filepath_import)
imported = {}

origin = {}
# origin data into json
with io.open(filepath_origin, 'rb') as f:
    reader = csv.reader(f, delimiter='\t', lineterminator='\n')
    for row in reader:
        if len(row) == 3:
            origin[row[0]] = {
                "mbid": row[0],
                "name": row[1],
                "country": row[2]
            }

for country in countries:
    processed_no = processed_no + 1
    imported[country['name']] = {}

    print ''
    print 'processing country: ' + country['name'] + ', ' + str(
        processed_no) + ' / ' + str(countries_no)

    for artist in country['artists']:
        mbid = artist['mbid']
        if mbid in origin:
            try:
                origin_country = origin[artist['mbid']]['country']

                if origin_country in imported[country['name']]:
                    imported[country['name']][origin_country] += 1

                else:
                    imported[country['name']][origin_country] = 1

            except Exception as e:
                print('artist without origin ' + artist['name'] + ' not found')

store_json(filepath_import, imported, True)