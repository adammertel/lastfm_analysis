import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import json
import csv
import io

lfm_api = '778ac0fc81473b52b8ca6c8c7f476e11'
limit_artists = 200
tag_threshold = 0.001
round_decimals = 1000000
values_to_store = ['name', 'country', 'age', 'gender', 'playcount']


def store_json(path, new_json, inform=False):
    with open(path, 'w') as file:
        json.dump(new_json, file)
        if inform:
            print 'file ' + path + ' saved.'


def do_as_request(url_rest):
    return do_request('http://ws.audioscrobbler.com/2.0/?method=' + url_rest +
                      '&api_key=' + lfm_api + '&format=json')


def do_request(url):
    return requests.get(url).json()


def get_friends(username):
    return do_as_request('user.getfriends&user=' + username)


def store_friends(usernames, lvl):
    new_users = []
    for ui, username in enumerate(usernames):
        print('progress: (lvl: ' + str(lvl) + ', user: ' + username + ') - ' +
              str(float(ui) / float(len(usernames)) * 100) + '%')

        friends_q = get_friends(username)
        try:
            if 'friends' in friends_q:
                friends = friends_q['friends']['user']

                for friend in friends:
                    name = friend['name']

                    friend_d = {}
                    for value in values_to_store:
                        friend_d[value] = friend[value]
                    friend_d['lvl'] = lvl

                    if name not in all_users:
                        new_users.append(name)
                        all_users[name] = friend_d
                    else:
                        print('user ' + username + ' in stored values already')

        except Exception as e:
            print('!!')
            print('problem reading user, ' + username + ' !!')
            print(e)
            print('!!')

    return new_users


all_users = {}

#first iteratiron
friends1 = store_friends(['Endar61'], 1)

#second iteration
friends2 = store_friends(friends1, 2)

#third iteration
friends3 = store_friends(friends2, 3)

with io.open('users.csv', 'wb') as f:
    writer = csv.writer(f, delimiter='\t', lineterminator='\n')

    writer.writerow(values_to_store)

    for user in all_users:
        user_row = []
        for value in values_to_store:
            user_row.append(all_users[user][value])

        user_row.append(all_users[user]['lvl'])
        writer.writerow(user_row)

store_json('users.json', all_users, True)