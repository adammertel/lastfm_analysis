import requests
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import json
import csv
import io

aggregated = {}

lvls = ['0', '1', '2', '3', 'sum']
with io.open('users.csv', 'rb') as f:
    reader = csv.reader(f, delimiter='\t', lineterminator='\n')
    for ri, row in enumerate(reader):
        if ri != 0:
            print(row)
            country = row[2]
            lvl = row[0]
            playcount = int(row[3])

            if country not in aggregated:
                aggregated[country] = {}
                for l in lvls:
                    aggregated[country][l] = {'users': 0, 'playcount': 0}

            aggregated[country]['sum']['playcount'] += playcount
            aggregated[country][lvl]['playcount'] += playcount

            aggregated[country]['sum']['users'] += 1
            aggregated[country][lvl]['users'] += 1

with open('users_aggregated.json', 'w') as file:
    json.dump(aggregated, file)