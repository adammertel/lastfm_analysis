import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import time

lfm_api = '778ac0fc81473b52b8ca6c8c7f476e11'
country = 'Slovakia'
requests.adapters.DEFAULT_RETRIES = 5

all_countries = {}
no_artists = 1000

artists_r = requests.get('http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country=' + country + '&api_key=' + lfm_api + '&format=json&limit=' + str(no_artists))
artists = artists_r.json()['topartists']['artist']

for ai, artist in enumerate(artists):
    if ai % 10 == 0:
        print('progress: ' + str(float(ai) / float(no_artists) * 100) + '%')

    try:
        band_id = artist['mbid']
        r_brainz = requests.get('http://musicbrainz.org/ws/2/artist/' + band_id + '?inc=aliases&fmt=json')
        
        if r_brainz.status_code == 503:
            time.sleep(10)
            r_brainz = requests.get('http://musicbrainz.org/ws/2/artist/' + band_id + '?inc=aliases&fmt=json')
        
        origin = 'unknown'
        if 'country' in r_brainz.json():
            origin = r_brainz.json()['country']
            
        print('origin: ' +  origin)

        if origin in all_countries:
            all_countries[origin] += 1
        else:
            all_countries[origin] = 1
    except:
        print('problem finding origins: ')
        print(artist)
        print('')
        no_artists -= 1
    
    time.sleep(1)



# normalise
for c in all_countries:
    all_countries[c] = float(all_countries[c]) / float(no_artists)

print(all_countries)

others_sum = 0
will_remove = []
for c in all_countries:
    if all_countries[c] < 0.01:
        others_sum += all_countries[c]
        will_remove.append(c)


for c in will_remove:
    del all_countries[c]

all_countries['other - less than 1%'] = others_sum
print(all_countries)


sorted_countries = []
sorted_values = []
for key, value in sorted(all_countries.iteritems(), key=lambda (k,v): (v,k)):
    sorted_countries.append(key)
    sorted_values.append(value)
    
fig1, ax1 = plt.subplots()
ax1.pie(sorted_values, labels=sorted_countries, autopct='%1.1f%%', colors=cm.Set1(np.linspace(0, 1, len(sorted_countries))))
ax1.axis('equal')
plt.show()