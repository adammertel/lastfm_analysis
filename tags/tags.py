import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import json
import csv
import io

lfm_api = '778ac0fc81473b52b8ca6c8c7f476e11'
limit_artists = 1000
round_decimals = 1000000

country_pop_limit = 200000
country_users_limit = 100


def do_as_request(url_rest):
    return do_request('http://ws.audioscrobbler.com/2.0/?method=' + url_rest +
                      '&api_key=' + lfm_api + '&format=json')


def do_request(url):
    return requests.get(url).json()


def append_object_to_stored_json(path, key, value):
    loaded_json = json.load(open(path))
    loaded_json[key] = value
    store_json(path, loaded_json)


def extend_stored_json(path, extension):
    loaded_json = json.load(open(path))
    extended_json = loaded_json.update(extension)
    store_json(path, extended_json)


def store_json(path, new_json, inform=False):
    with open(path, 'w') as file:
        json.dump(new_json, file)
        if inform:
            print 'file ' + path + ' saved.'


def clean_json(path):
    store_json(path, {})


def clean_tag_name(tag):
    if tag == 'rhythm and blues':
        tag = 'rnb'
    return tag.lower().replace('-', ' ').replace('\'', '').replace('&', 'n')


def _round(number, places=round_decimals):
    return float(float(int(number * places)) / float(places))


# parse countries_tags
def parse_and_store():
    parsed_countries_tags = {}
    tags_keys = {}
    next_id = 1

    def find_tag_in_tags_keys(tag):
        for key in tags_keys:
            if tags_keys[key]['name'] == tag:
                return key
        return False

    parse1 = 0
    for country in countries_tags:
        parse1 += 1
        print('parsing1: ' +
              str(_round(float(parse1) / float(countries_no) * 100, 2)) + '%')

        # creating list of tags
        for tag in countries_tags[country]:

            parsed_tag_id = find_tag_in_tags_keys(tag)
            if parsed_tag_id:
                tags_keys[parsed_tag_id]['val'] += _round(
                    countries_tags[country][tag])

            else:
                tags_keys[next_id] = {
                    "name": tag,
                    "val": _round(countries_tags[country][tag])
                }
                next_id = next_id + 1

    # normalise
    normalised_relevant_tags = {}
    for key in tags_keys:
        tags_keys[key]['val'] = _round(
            float(tags_keys[key]['val']) / float(len(countries_tags.keys())))

        normalised_relevant_tags[key] = tags_keys[key]

    tags_keys = normalised_relevant_tags

    parse2 = 0
    for country in countries_tags:
        parse2 += 1
        print('parsing2: ' +
              str(_round(float(parse2) / float(countries_no) * 100, 2)) + '%')

        parsed_countries_tags[country] = {}
        for tag in countries_tags[country]:
            tag_id = find_tag_in_tags_keys(tag)
            if tag_id:
                parsed_countries_tags[country][tag_id] = float(
                    countries_tags[country][tag])

    print(sum(tags_keys[i]['val'] for i in tags_keys))

    # storing output
    store_json('countries_tags.json', parsed_countries_tags, True)
    store_json('tags_list.json', tags_keys, True)
    store_json('countries_not_found.json', countries_not_found, True)


# cleaning old data
#clean_json('artists_tags.json')
clean_json('countries_tags.json')
clean_json('countries_not_found.json')
print('lists cleaned')

countries_tags = {}
artists_tags = json.load(open('artists_tags.json'))
countries = json.load(open('./../countries.geojson'))
countries_users = json.load(open('./../users/users_aggregated.json'))

# creating white list
white_list = []
with open('white_list.txt', 'rb') as file:
    reader = csv.reader(file, delimiter='\t', lineterminator='\n')
    for row in reader:
        white_list.append(clean_tag_name(row[0]))

#
countries_not_found = []

countries_reduced = []
for c in countries['features']:
    props = c['properties']
    country_users = False

    if props['admin'] in countries_users:
        country_users = countries_users[props['admin']]
    elif props['NAME'] in countries_users:
        country_users = countries_users[props['NAME']]

    if country_users and c['properties']['POP_EST'] > country_pop_limit and country_users['sum']['users'] > country_users_limit:
        countries_reduced.append(c)

print [c['properties']['admin'] for c in countries_reduced]

countries_no = len(countries_reduced)
processed_no = 0

for country_obj in countries_reduced:
    processed_no = processed_no + 1
    country = country_obj['properties']['admin']

    print ''
    print 'processing country: ' + country + ', ' + str(
        processed_no) + ' / ' + str(countries_no)

    country_tags = {}
    found_artists = limit_artists

    artists = False

    try:
        artists_q = do_as_request('geo.gettopartists&country=' + country +
                                  '&limit=' + str(limit_artists))

        # in case, the 'admin' property is not good, use the NAME
        if 'topartists' not in artists_q:
            artists_q = do_as_request(
                'geo.gettopartists&country=' + country_obj['properties']
                ['NAME'] + '&limit=' + str(limit_artists))

        artists = artists_q['topartists']['artist']

        for ai, artist in enumerate(artists):
            if ai % 25 == 0 and ai != 0:
                print('progress: (' + country + ') - ' +
                      str(float(ai) / float(limit_artists) * 100) + '%')

            artist_weight = 1 - float(ai) / float(limit_artists)
            artist_tags = {}

            if (artist['name'] in artists_tags):
                artist_tags = artists_tags[artist['name']]

            else:
                artist_tags_raw = do_as_request(
                    'artist.gettoptags&mbid=' + artist['mbid'])

                if 'toptags' in artist_tags_raw:
                    tags_list = artist_tags_raw['toptags']['tag']

                    allowed_tags = [
                        d for d in tags_list
                        if clean_tag_name(d['name']) in white_list
                    ]
                    sum_count = sum(i['count'] for i in allowed_tags)

                    for tag in allowed_tags:
                        tag_name = clean_tag_name(tag['name'])
                        artist_tags[tag_name] = _round(
                            float(tag['count']) / float(sum_count))

                    append_object_to_stored_json('artists_tags.json',
                                                 artist['name'], artist_tags)
                    print('artist ' + artist['name'] + ' added to stored list')

                else:
                    found_artists = found_artists - 1

            for tag_name in artist_tags:
                if tag_name not in country_tags:
                    country_tags[tag_name] = artist_tags[
                        tag_name] * artist_weight
                else:
                    country_tags[tag_name] += artist_tags[
                        tag_name] * artist_weight

            artists_tags[artist['name']] = artist_tags

        # remove small
        relevant_tags = {}
        for tag in country_tags:
            relevant_tags[tag] = country_tags[tag]

        # normalise
        sum_relevant_tags = sum(relevant_tags[i] for i in relevant_tags)
        country_tags_normal = {}

        for tag in relevant_tags:
            country_tags_normal[tag] = _round(
                relevant_tags[tag] / sum_relevant_tags)

        countries_tags[country] = country_tags_normal

    except Exception as e:
        print('!!')
        print('problem reading country, ' + country + ' !!')
        print(e)
        print('!!')
        countries_not_found.append(country)
        countries_tags[country] = {}

    #if processed_no == 3:
    #parse_and_store()
    #break

parse_and_store()

# others_sum = 0
# will_remove_tags = []
# for tag in all_tags:
#     if all_tags[tag] < 0.01:
#         others_sum += all_tags[tag]
#         will_remove_tags.append(tag)

# for tag in will_remove_tags:
#     del all_tags[tag]

# all_tags['other - less than 1%'] = others_sum

# sorted_tags = []
# sorted_values = []
# for key, value in sorted(all_tags.iteritems(), key=lambda (k, v): (v, k)):
#     sorted_tags.append(key)
#     sorted_values.append(value)

# fig1, ax1 = plt.subplots()
# ax1.pie(
#     sorted_values,
#     labels=sorted_tags,
#     autopct='%1.1f%%',
#     colors=cm.Set1(np.linspace(0, 1, len(sorted_tags))))
# ax1.axis('equal')
# plt.show()