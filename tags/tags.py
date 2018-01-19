import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import json

lfm_api = '778ac0fc81473b52b8ca6c8c7f476e11'
limit_artists = 1
tag_threshold = 0.001


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
    return tag.lower().replace('-', ' ').replace('\'', '')


# cleaning old data
clean_json('artists_tags.json')
clean_json('countries_tags.json')
clean_json('countries_not_found.json')
print('lists cleaned')

countries_tags = {}
artists_tags = json.load(open('artists_tags.json'))
countries = json.load(open('./../countries.geojson'))

# adding country names to the list of restricted tags
restricted_tags = json.load(open('restricted_tags.json'))
country_names = [
    c['properties']['admin'].lower() for c in countries['features']
]
restricted_tags += country_names

countries_not_found = []

processed_no = 0
for country_obj in countries['features']:
    processed_no = processed_no + 1
    country = country_obj['properties']['admin']

    print ''
    print 'processing country: ' + country + ', ' + str(
        processed_no) + ' / ' + str(len(countries['features']))

    country_tags = {}
    found_artists = limit_artists

    artists = False

    try:
        artists_q = do_as_request('geo.gettopartists&country=' + country +
                                  '&limit=' + str(limit_artists))
        artists = artists_q['topartists']['artist']

        for ai, artist in enumerate(artists):
            if ai % 10 == 0:
                print('progress: ' +
                      str(float(ai) / float(limit_artists) * 100) + '%')

            artist_tags = {}
            if (artist['name'] in artists_tags):
                artist_tags = artists_tags[artist['name']]

            else:
                artist_tags_raw = do_as_request(
                    'artist.gettoptags&artist=' + artist['name'])

                if 'toptags' in artist_tags_raw:
                    tags_list = artist_tags_raw['toptags']['tag']

                    allowed_tags = [
                        d for d in tags_list
                        if clean_tag_name(d['name']) not in restricted_tags
                    ]
                    sum_count = sum(i['count'] for i in allowed_tags)

                    for tag in allowed_tags:
                        tag_name = clean_tag_name(tag['name'])
                        artist_tags[tag_name] = float(
                            tag['count']) / float(sum_count)

                    append_object_to_stored_json('artists_tags.json',
                                                 artist['name'], artist_tags)
                    print('artist ' + artist['name'] + ' added to stored list')

                else:
                    found_artists = found_artists - 1

            for tag_name in artist_tags:
                if tag_name not in country_tags:
                    country_tags[tag_name] = artist_tags[tag_name]
                else:
                    country_tags[tag_name] += artist_tags[tag_name]

            artists_tags[artist['name']] = artist_tags

        # normalise, round and remove small
        country_tags_normal = {}
        for tag in country_tags:
            country_tags_normal[tag] = float("{0:.5f}".format(
                country_tags[tag] / found_artists))

            # if small
            if country_tags_normal[tag] < tag_threshold:
                try:
                    del country_tags_normal[tag]
                except:
                    print 'problem removing tag ' + tag

        countries_tags[country] = country_tags_normal

    except:
        countries_not_found.append(country)
        countries_tags[country] = {}

    #if processed_no == 10:
    #break

# parse countries_tags
parsed_countries_tags = {}
tags_keys = {}
next_id = 1


def find_tag_in_tags_keys(tag):
    found = False
    for key in tags_keys:
        if tags_keys[key]['name'] == tag:
            found = key
    return found


for country in countries_tags:
    for tag in countries_tags[country]:

        parsed_tag_id = find_tag_in_tags_keys(tag)
        if parsed_tag_id:
            tags_keys[parsed_tag_id]['val'] += float(
                countries_tags[country][tag])

        else:
            tags_keys[next_id] = {
                "name": tag,
                "val": float(countries_tags[country][tag])
            }
            next_id = next_id + 1

for country in countries_tags:
    parsed_countries_tags[country] = {}
    for tag in countries_tags[country]:
        tag_id = find_tag_in_tags_keys(tag)
        parsed_countries_tags[country][tag_id] = countries_tags[country][tag]

# storing output
store_json('countries_tags.json', parsed_countries_tags, True)
store_json('tags_list.json', tags_keys, True)
store_json('countries_not_found.json', countries_not_found, True)

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