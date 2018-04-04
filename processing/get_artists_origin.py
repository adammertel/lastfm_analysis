from base import *

filepath_origin = './data/artists_origin.csv'
filepath_no_data_origin = './data/artists_origin_nodata.csv'
filepath_manual_origin = './data/artists_origin_manual.csv'
filepath_countries_topartists = './data/countries_topartists1000.json'

countries = json.load(open(filepath_countries_topartists))

countries_no = len(countries)
processed_no = 0

origin_all = {}

# previously stored
with io.open(filepath_origin, 'rb') as f:
    reader = csv.reader(f, delimiter='\t', lineterminator='\n')
    for row in reader:
        if len(row) == 3:
            origin_all[row[0]] = {
                "mbid": row[0],
                "name": row[1],
                "origin": row[2]
            }

# manually added
with io.open(filepath_manual_origin, 'rb') as f:
    reader = csv.reader(f, delimiter='\t', lineterminator='\n')
    for row in reader:
        print(row)
        if len(row) == 3:
            origin_all[row[0]] = {
                "mbid": row[0],
                "name": row[1],
                "origin": row[2]
            }


def store_origins():
    with io.open(filepath_origin, 'wb') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        for ai in origin_all:
            artist = origin_all[ai]
            if artist['origin']:
                try:
                    writer.writerow([
                        clean_str(artist['mbid']),
                        clean_str(artist['name']),
                        clean_str(artist['origin'])
                    ])
                except Exception as e:
                    print('problem storing artist' + artist['name'])


for country in countries:
    processed_no = processed_no + 1

    print ''
    print 'processing country: ' + country['name'] + ', ' + str(
        processed_no) + ' / ' + str(countries_no)

    for ai, artist in enumerate(country['artists']):
        if ai % 100 == 0 and ai != 0:
            print('progress: (' + country['name'] + ') - ' +
                  str(float(ai) / float(1000) * 100) + '%')

        if artist['mbid'] not in origin_all:
            try:
                if artist['mbid']:
                    mb = request_mb(artist['mbid'])
                    if 'error' in mb:
                        time.sleep(0.5)
                        mb = request_mb(artist['mbid'])

                    if 'country' in mb:
                        origin = mb['country']

                        origin_all[artist['mbid']] = {
                            "mbid": artist['mbid'],
                            "name": artist['name'],
                            "origin": origin
                        }

            except Exception as e:
                print('artist without origin ' + artist['name'] + ' not found')

    store_origins()

with io.open(filepath_no_data_origin, 'wb') as f:
    writer = csv.writer(f, delimiter='\t', lineterminator='\n')
    for ai in origin_all:
        artist = origin_all[ai]
        if not artist['origin']:
            try:
                writer.writerow([
                    clean_str(artist['mbid']),
                    clean_str(artist['name']),
                ])

            except Exception as e:
                print('problem storing artist' + artist['name'])
