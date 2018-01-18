import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import json

lfm_api = '778ac0fc81473b52b8ca6c8c7f476e11'
country = 'Portugal'

all_tags = {}
no_artists = 100

artists_tags = json.load(open('tags.json'))

artists_r = requests.get('http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country=' + country + '&api_key=' + lfm_api + '&format=json&limit=' + str(no_artists))
artists = artists_r.json()['topartists']['artist']

for ai, artist in enumerate(artists):
    if ai % 10 == 0:
        print('progress: ' + str(float(ai) / float(no_artists) * 100) + '%')

    artist_tags = {}
    if (artist['name'] in artists_tags):
        artist_tags = artists_tags[artist['name']]
        print('artist '  + artist['name'] +  ' loaded from stored json')

    else:
        r_tags = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=' + artist['name'] + '&api_key=' + lfm_api + '&format=json')
        
        if 'toptags' in r_tags.json():
            tags_list = r_tags.json()['toptags']['tag']
            
            sum_count = sum(i['count'] for i in tags_list)

            for tag in tags_list:
                tag_name = tag['name'].lower()
                artist_tags[tag_name] = float(tag['count']) / float(sum_count)
        else: 
            no_artists = no_artists - 1

    for tag in tags_list:
        if tag_name not in all_tags:
            all_tags[tag_name] = float(tag['count']) / float(sum_count)
        else:
            all_tags[tag_name] += float(tag['count']) / float(sum_count)

    artists_tags[artist['name']] = artist_tags

with open('tags.json', 'w') as file_tags:
    json.dump(artists_tags, file_tags)


# normalise
for tag in all_tags:
    all_tags[tag] = all_tags[tag] / no_artists

others_sum = 0
will_remove_tags = []
for tag in all_tags:
    if all_tags[tag] < 0.01:
        others_sum += all_tags[tag]
        will_remove_tags.append(tag)


for tag in will_remove_tags:
    del all_tags[tag]

all_tags['other - less than 1%'] = others_sum


sorted_tags = []
sorted_values = []
for key, value in sorted(all_tags.iteritems(), key=lambda (k,v): (v,k)):
    sorted_tags.append(key)
    sorted_values.append(value)
    
fig1, ax1 = plt.subplots()
ax1.pie(sorted_values, labels=sorted_tags, autopct='%1.1f%%', colors=cm.Set1(np.linspace(0, 1, len(sorted_tags))))
ax1.axis('equal')
plt.show()