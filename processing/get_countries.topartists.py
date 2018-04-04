from base import *

filepath_not_found = './data/countries_notfound.json'
filepath_top = './data/countries_topartists1000.json'

clean_json(filepath_not_found)
clean_json(filepath_top)
no_artists = 1000

countries = get_countries(100000, 50)
countries_topartists = []

countries_no = len(countries)
processed_no = 0

countries_not_found = []


def construct_url(country_name):
    return 'geo.gettopartists&country=' + country_name + '&limit=' + str(
        no_artists)


for country in countries:
    processed_no = processed_no + 1
    country_name = country['properties']['admin']
    country_name_alt = country['properties']['NAME']

    print ''
    print 'processing country: ' + country_name + ', ' + str(
        processed_no) + ' / ' + str(countries_no)

    artists = []

    try:
        artists_q = request_lfm(construct_url(country_name))

        if 'topartists' not in artists_q:
            artists_q = request_lfm(construct_url(country_name_alt))

        found_artists = artists_q['topartists']['artist']

        for ai, artist in enumerate(found_artists):
            artist_dict = {
                "name": artist['name'],
                "mbid": artist['mbid'],
                "no": ai,
                "url": artist['url']
            }
            artists.append(artist_dict)

        countries_topartists.append({"name": country_name, "artists": artists})

    except Exception as e:
        print('country ' + country_name + ' not found')
        countries_not_found.append(country_name)

store_json(filepath_not_found, countries_not_found, True)
store_json(filepath_top, countries_topartists, True)
