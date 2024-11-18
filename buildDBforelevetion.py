import  pickle
import time

import requests
import osmnx as ox
import graphBuilding
import os

city_graph = ox.graph_from_place("Jerusalem", network_type="bike")
nodes = city_graph.nodes()
edges = city_graph.edges(data=True)

def add_elevation_data_to_the_dict(lat, lon, data, elevation_dict):
    if lat not in elevation_dict:
        elevation_dict[lat] = {}
        if lon not in elevation_dict[lat]:
            elevation_dict[lat][lon] = {}
    elevation_dict[lat][lon] = data

#build the dict
elevation_dict = {}

for node, data in city_graph.nodes(data=True):
    lat = data['y']
    lon = data['x']
    elevation = graphBuilding.get_elevetion_from_osmnx(lat, lon)
    add_elevation_data_to_the_dict(lat, lon, elevation, elevation_dict)
    time.sleep(1)

#now we want to save this dict in a file with pickle
with open("elevation_dict.pkl", 'wb') as file:
    pickle.dump(elevation_dict, file)

#now we want to load the dict from the file
with open("elevation_dict.pkl", 'rb') as file:
    elevation_dict = pickle.load(file)


print(len(elevation_dict))
counter = 0
for key in elevation_dict:
    print(counter, ": " ,elevation_dict[key])
