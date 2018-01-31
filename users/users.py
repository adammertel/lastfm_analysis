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
processing_lvl = 0
will_process = []
start_user = 'Endar61'

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


def do_as_request(url_rest):
    return do_request('http://ws.audioscrobbler.com/2.0/?method=' + url_rest +
                      '&api_key=' + lfm_api + '&format=json')


def do_request(url):
    return requests.get(url).json()


def get_friends(username):
    return do_as_request('user.getfriends&user=' + username)


total = 0
new = 0


def store_friends():
    global total
    global new

    this_lvl_users = []
    lvl = 0

    with io.open('next_level.csv', 'rb') as f:
        reader = csv.reader(f, delimiter='\t', lineterminator='\n')
        for ri, row in enumerate(reader):
            if ri == 0:
                lvl = int(row[0])
            else:
                this_lvl_users.append(row[0])

    if len(this_lvl_users) == 0:
        this_lvl_users = [start_user]

    for_the_next_lvl = []

    will_be_stored = []

    for ui, username in enumerate(this_lvl_users):
        print('progress: (lvl: ' + str(lvl) + ', user: ' + username + ') - ' +
              str(float(ui) / float(len(this_lvl_users)) * 100) + '%')

        friends_q = get_friends(username)
        try:
            if 'friends' in friends_q:
                processed_users.append(username)
                friends = friends_q['friends']['user']

                stored = 0
                for friend in friends:
                    name = friend['name']

                    if name not in stored_users:
                        stored_users.append(name)
                        will_be_stored.append([
                            friend['name'], lvl, friend['country'],
                            friend['playcount']
                        ])
                        stored += 1

                    if name not in processed_users:
                        for_the_next_lvl.append(name)

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

    # saving processed users
    with io.open('processed.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        for processed_user in processed_users:
            writer.writerow([processed_user])

    # storing found friends
    with io.open('users.csv', 'ab') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        for friend in will_be_stored:
            writer.writerow(friend)

    # storing users to be processed in the next iteration
    lvl += 1
    with io.open('next_level.csv', 'wb') as f:
        writer = csv.writer(f, delimiter='\t', lineterminator='\n')
        writer.writerow(str(lvl))
        for user in for_the_next_lvl:
            writer.writerow([user])

    if lvl < 8:
        store_friends()


store_friends()
