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
values_to_store = ['name', 'country', 'playcount']

stored_users = []
processed_users = []

with io.open('users.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t', lineterminator='\n')
    for row in reader:
        stored_users.append(row[0])

with io.open('processed.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t', lineterminator='\n')
    for row in reader:
        processed_users.append(row[0])

print(len(stored_users))
print(len(processed_users))


def store_new_user(username, user_data):
    stored_users.append(username)

    with io.open('users.csv', 'ab') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(user_data)


def do_as_request(url_rest):
    return do_request('http://ws.audioscrobbler.com/2.0/?method=' + url_rest +
                      '&api_key=' + lfm_api + '&format=json')


def do_request(url):
    return requests.get(url).json()


def get_friends(username):
    return do_as_request('user.getfriends&user=' + username)


total = 0
new = 0


def store_friends(usernames, lvl):
    global total
    global new

    new_users = []
    for ui, username in enumerate(usernames):
        #print('progress: (lvl: ' + str(lvl) + ', user: ' + username + ') - ' +
        #str(float(ui) / float(len(usernames)) * 100) + '%')

        friends_q = get_friends(username)
        try:
            if 'friends' in friends_q:
                friends = friends_q['friends']['user']

                stored = 0
                for friend in friends:
                    name = friend['name']

                    if name not in stored_users:
                        store_new_user(name, [
                            friend['name'], lvl, friend['country'],
                            friend['playcount']
                        ])
                        stored += 1

                    if name not in processed_users:
                        new_users.append(name)

                total += len(friends)
                new += stored

                print('user: ' + username + ' , lvl: ' + str(lvl) + ' stored '
                      + str(stored) + '/' + str(len(friends)) + ', total: ' +
                      str(len(stored_users)) + ' [success rate: ' + str(
                          (float(new) / float(total)) * 100) + '%]')

        except Exception as e:
            print('!!')
            print('problem reading user, ' + username + ' !!')
            print(e)
            print('!!')

        if username not in processed_users:
            processed_users.append(username)
            with io.open('processed.csv', 'ab') as f:
                writer = csv.writer(f, delimiter='\t', lineterminator='\n')
                writer.writerow([username])

    return new_users


# first iteratiron
friends1 = store_friends(['mIZZYchal'], 1)

# second iteration
friends2 = store_friends(friends1, 2)

# third iteration
friends3 = store_friends(friends2, 3)

# fourth iteration
friends4 = store_friends(friends3, 4)
#friends5 = store_friends(friends4, 5)
#friends6 = store_friends(friends5, 6)
