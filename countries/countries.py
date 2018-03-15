import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import json
import csv
import io

lfm_api = '778ac0fc81473b52b8ca6c8c7f476e11'
requests.adapters.DEFAULT_RETRIES = 5
no_artists = 10
country_pop_limit = 200000
country_users_limit = 100


def request_lfm(url_rest):
    return do_request('http://ws.audioscrobbler.com/2.0/?method=' + url_rest +
                      '&api_key=' + lfm_api + '&format=json')


def request_mb(mbid):
    return do_request(
        'http://musicbrainz.org/ws/2/artist/' + mbid + '?inc=aliases&fmt=json')


def do_request(url):
    print(url)
    return requests.get(url).json()


all_countries = {}
bands_not_found = {}
bands_saved = {}
countries_not_found = []

countries = json.load(open('./../countries.geojson'))
countries_users = json.load(open('./../users/users_aggregated.json'))

countries_r = []
for c in countries['features']:
    props = c['properties']
    country_users = False

    if props['admin'] in countries_users:
        country_users = countries_users[props['admin']]
    elif props['NAME'] in countries_users:
        country_users = countries_users[props['NAME']]

    if country_users and c['properties']['POP_EST'] > country_pop_limit and country_users['sum']['users'] > country_users_limit:
        countries_r.append(c)

countries_no = len(countries_r)
processed_no = 0

for country_obj in countries_r:
    processed_no = processed_no + 1
    country_name = country_obj['properties']['admin']
    country = {}

    print ''
    print 'processing country: ' + country_name + ', ' + str(
        processed_no) + ' / ' + str(countries_no)

    artists = []
    try:
        artists_q = request_lfm('geo.gettopartists&country=' + country_name +
                                '&limit=' + str(no_artists))
        artists = artists_q['topartists']['artist']

    except Exception as e:
        print('country ' + country_name + ' not found')
        countries_not_found.append(country_name)

    for ai, artist in enumerate(artists):
        if ai % 25 == 0 and ai != 0:
            print('progress: (' + country_name + ') - ' +
                  str(float(ai) / float(no_artists) * 100) + '%')

        artist_weight = 1 - float(ai) / float(no_artists)

        mbid = artist['mbid']
        a_name = artist['name']

        origin = False

        if mbid in bands_saved:
            origin = bands_saved[mbid]['origin']
        else:
            try:
                mb = request_mb(mbid)
                print(mb)
                origin = mb['country']

                bands_saved[mbid] = {origin: origin, name: a_name}

            except Exception as e:
                print('mb problem: ' + a_name)

        if origin:
            if origin in country:
                country[origin] += 1
            else:
                country[origin] = 1
        else:
            bands_not_found[mbid] = {name: a_name}
