import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import json
import csv
import unicodecsv as csv
import io
import time

lfm_api = '778ac0fc81473b52b8ca6c8c7f476e11'
requests.adapters.DEFAULT_RETRIES = 5


def clean_str(str):
    return str.encode('utf8')


def request_lfm(url_rest):
    return do_request('http://ws.audioscrobbler.com/2.0/?method=' + url_rest +
                      '&api_key=' + lfm_api + '&format=json')


def request_mb(mbid):
    return do_request(
        'http://musicbrainz.org/ws/2/artist/' + mbid + '?inc=aliases&fmt=json',
        False)


def do_request(url, showUrl=True):
    if showUrl:
        print(url)
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


def get_countries(country_pop_limit=200000, country_users_limit=100):
    countries = json.load(open('./data/countries_full.geojson'))
    countries_users = json.load(open('./data/countries_users.json'))

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

    return countries_r