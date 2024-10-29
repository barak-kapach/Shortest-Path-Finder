import rasterio as rio

import osmnx as ox
import requests
from networkx import desargues_graph

"""
    in this file we will build the graph of the city and add the weight to the edges.
    the weight will be based on the height difference and the length of the path.
"""

# get the graph of the city
city = "Jerusalem, Israel"
city_graph = ox.graph_from_place("Jerusalem, Israel", network_type="bike")

# get the nodes of the city and create a photo - to see the city
nodes = city_graph.nodes()
ox.plot_graph(city_graph)

print("done  ! ", len(nodes))

edges = city_graph.edges(data=True)


# add weight to edges

# add weight to edges with tiff file
# city_graph = ox.add_node_elevations_raster(city_graph, r"C:\Users\user\PycharmProjects\MapsHeightBase.tif")

# add weight to edges with Google api
# city_graph = ox.add_node_elevations_google(city_graph)

def add_elevation_to_nodes(G, api_key):
    # Get the list of nodes
    nodes = list(G.nodes(data=True))

    # Prepare the list of coordinates
    coordinates = [(data['y'], data['x']) for node, data in nodes]

    # Use the Google Elevation API to get elevation data
    elevation_data = get_elevation_data(coordinates, api_key)

    # Add elevation data to the nodes
    for (node, data), elevation in zip(nodes, elevation_data):
        G.nodes[node]['elevation'] = elevation

    return G


def get_elevation_data(coordinates, api_key):
    url = 'https://maps.googleapis.com/maps/api/elevation/json'
    elevations = []

    for lat, lon in coordinates:
        params = {
            'locations': f'{lat},{lon}',
            'key': api_key
        }
        response = requests.get(url, params=params)
        results = response.json().get('results', [])
        if results:
            elevations.append(results[0]['elevation'])
        else:
            elevations.append(None)

    return elevations


def add_elevation_data_to_the_graph():
    for u, v, key, data in city_graph.edges(data=True, keys=True):
        elev_u = city_graph.nodes[u]['elevation']
        elev_v = city_graph.nodes[v]['elevation']
        data['height_diff'] = elev_v - elev_u
        # we don't use abs because in the weight func we want to know if we are going up or down
        print(data['height_diff'])


# build a weight function - we want to give the best path for bikes, based on the height difference and the length of the path
def bike_weight_func(u, v, data):
    # get the length
    length = data['length']
    # we already have the height difference, we want to give it a weight
    height_diff = data['height_diff']
    if height_diff > 0:
        # going up
        data['weight'] = length + 100 * height_diff
    else:
        # going down
        data['weight'] = max(1, abs(length + (height_diff * 2)))  # (height * 2) is a negative number

    return data['weight']


def add_weight_to_the_graph(city_graph, weight_func):
    for u, v, key, data in city_graph.edges(data=True, keys=True):
        data['weight'] = weight_func(u, v, data)


def get_city_graph():
    return city_graph

# add_elevation_to_nodes(city_graph, "AIzaSyAHXqjPhuRDQVflHiW4V8ly_w580NE_eOc")

#here we want to create function that get info from user like city, country and build the graph
# def get_city_graph(city, country):
#     city_graph = ox.graph_from_place(f"{city}, {country}", network_type="bike")
#     return city_graph



#
# # add the weight to the edges - we want to give the best path for bikes
# for u, v, key, data in city_graph.edges(data=True, keys=True):
#     data['weight'] = bike_weight_func(u, v, data)

#     print(data['weight'], "this is the weight")


# # now we want to test our func with some origin and destination
# origin = list(city_graph.nodes())[0]
# n = len(list(city_graph.nodes()))
# ind = n // 2
# destination = list(city_graph.nodes())[ind]
# path = get_shortest_path(city_graph, origin, destination)
# for i in range(len(path)):
#     print(i,  path[i])
# print(type(path)) #class list

# add_elevation_to_nodes(city_graph, "AIzaSyA2a5j-AIzaSyAHXqjPhuRDQVflHiW4V8ly_w580NE_eOc")
# add_elevation_data_to_the_graph()
# add_weight_to_the_graph(city_graph, bike_weight_func)


# # now we want to add the evaluation difference to the edges
# for u, v, key, data in city_graph.edges(data=True, keys=True):
#     elev_u = city_graph.nodes[u]['elevation']
#     elev_v = city_graph.nodes[v]['elevation']
#     data['height_diff'] = elev_v - elev_u
#     # we don't use abs because in the weight func we want to know if we are going up or down
#     print(data['height_diff'])
