import pickle
import time
import osmnx as ox
from matplotlib.pyplot import yticks
from pyhigh import get_elevation
import requests



"""
    in this file we will build the graph of the city and add the weight to the edges.
    the weight will be based on the height difference and the length of the path.
"""

def add_height_diff_to_edges(city_graph):
    for u, v, key, data in city_graph.edges(data=True, keys=True):
        elev_v = city_graph.nodes[v]['elevation']
        elev_u = city_graph.nodes[u]['elevation']
        # print(elev_v, elev_u)
        data['height_diff'] = elev_v - elev_u
        # print(data['height_diff'])
    return city_graph


# build a weight function - we want to give the best path for bikes, based on the height difference and the length of the path
def bike_weight_func(u, v, data, hills_factor=1):
    # get the length
    length = data.get('length', 1)
    # we already have the height difference, we want to give it a weight
    height_diff = data.get('height_diff', 0)
    if height_diff > 0:
        # going up
        data['weight'] = length +  height_diff**hills_factor
    else:
        # going down
        data['weight'] = max(1, abs(length + (height_diff * 2 * hills_factor)))  # (height * 2) is a negative number

    return data['weight']

def add_weight_to_the_graph(city_graph, weight_func, hills_factor=1):
    for u, v, key, data in city_graph.edges(data=True, keys=True):
        data['weight'] = weight_func(u, v, data, hills_factor)
    return city_graph


def get_elevetion_from_osmnx(lat, lon):
    url = f"https://api.opentopodata.org/v1/srtm90m?locations={lat},{lon}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0]['elevation']
    return None



def add_elevation_data_with_osmnx(graph):
    # iterate over the nodes
    counter = 0
    for node, data in graph.nodes(data=True):
        lat = data['y']
        lon = data['x']
        elevation = get_elevetion_from_osmnx(lat, lon)
        print(counter, "eleveation: ", elevation)
        counter += 1
        if elevation is not None:
            graph.nodes[node]['elevation'] = elevation
        else:
            graph.nodes[node]['elevation'] = 0
        # to avoid the limit of the api request -> "error": "Per-second rate limit exceeded for the free hosted API.
        time.sleep(1)
    return graph


def add_elevation_data_to_the_graph_with_local_elevation_dict(graph):
    #load the pickle file
    with open("elevation_dict.pkl", "rb") as f:
        elevation_dict = pickle.load(f)
    lst_of_nodes_that_dont_have_elevation = []
    for node, data in graph.nodes(data=True):
        lat = data['y']
        lon = data['x']
        #check if the lat and lon are in the dict
        if lat in elevation_dict and lon in elevation_dict[lat]:
            elev = elevation_dict[lat][lon]
        else:
            lst_of_nodes_that_dont_have_elevation.append((lat, lon))
            elev = 0
            # node = ox.nearest_nodes(graph, lon, lat)
            # print("node", node)
            # lon, lat = node['y'], node['x']
            # elev = elevation_dict[lat][lon]
        # try:
        #     elev = elevation_dict[lat][lon]
        # except KeyError:
        #     node = ox.nearest_nodes(graph, lon, lat)
        #     lat, lon = graph.nodes[node]['y'], graph.nodes[node]['x']
        #     elev = elevation_dict[lat][lon]
        #     print("KeyError")
        graph.nodes[node]['elevation'] = elev
    print("")
    print(lst_of_nodes_that_dont_have_elevation)
    print(len(lst_of_nodes_that_dont_have_elevation))
    return graph

def get_graph_with_elevation_from_local(city, slope_value=1):
    graph = ox.graph_from_place(city, network_type="bike")
    print("Got the graph")
    graph = add_elevation_data_to_the_graph_with_local_elevation_dict(graph)
    print("Added the elevation data")
    graph = add_height_diff_to_edges(graph)
    print("Added the height difference")
    graph = add_weight_to_the_graph(graph, bike_weight_func, slope_value)
    return graph

# if __name__ == '__main__':
#     #test the functions
#     city_graph = get_graph_with_elevation_from_local("Jerusalem")





#
# from googlemaps.elevation import elevation
# from networkx import desargues_graph, nodes
# import rasterio as rio
# import googlemaps
#
# def add_elevation_data_with_osmnx(graph):
#     return asyncio.run(add_elevation_data_with_osmnx_async(graph))

# if __name__ == '__main__':
# print("hello")
# city_graph,  nodes, edges = get_city_graph_nodes_and_edges("Jerusalem")
# print("Got the graph")
# city_graph = add_elevation_data_with_osmnx(city_graph)
# for node in nodes:
#     print(node, city_graph.nodes[node])
#     print("node elevation", city_graph.nodes[node]['elevation'])

# city_graph = get_city_graph_with_elevation("Jerusalem")
# print(city_graph)
# print(city_graph.nodes(data=True))
# print(city_graph.edges(data=True))

# add weight to edges

# add weight to edges with tiff file
# city_graph = ox.add_node_elevations_raster(city_graph, r"C:\Users\user\PycharmProjects\MapsHeightBase.tif")

# add weight to edges with Google api
# city_graph = ox.add_node_elevations_google(city_graph)

# def add_elevation_to_nodes(G, api_key):
#     # Get the list of nodes
#     nodes = list(G.nodes(data=True))
#
#     # Prepare the list of coordinates
#     coordinates = [(data['y'], data['x']) for node, data in nodes]
#
#     # Use the Google Elevation API to get elevation data
#     elevation_data = get_elevation_data(coordinates, api_key)
#
#     # Add elevation data to the nodes
#     for (node, data), elevation in zip(nodes, elevation_data):
#         G.nodes[node]['elevation'] = elevation
#
#     return G
#
#
# def get_elevation_data(coordinates, api_key):
#     url = 'https://maps.googleapis.com/maps/api/elevation/json'
#     elevations = []
#
#     for lat, lon in coordinates:
#         params = {
#             'locations': f'{lat},{lon}',
#             'key': api_key
#         }
#         response = requests.get(url, params=params)
#         results = response.json().get('results', [])
#         if results:
#             elevations.append(results[0]['elevation'])
#         else:
#             elevations.append(None)
#
#     return elevations


# add_elevation_to_nodes(city_graph, "AIzaSyAHXqjPhuRDQVflHiW4V8ly_w580NE_eOc")

# here we want to create function that get info from user like city, country and build the graph
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


#
# async def fetch_elevation(session, lat, lon):
#     url = f"https://api.opentopodata.org/v1/srtm90m?locations={lat},{lon}"
#     async with session.get(url) as response:
#         if response.status == 200:
#             results = await response.json()
#             return results.get('results', [])[0]['elevation']
#         return None
#
#
# async def add_elevation_data_with_osmnx_async(graph):
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for node, data in graph.nodes(data=True):
#             lat = data['y']
#             lon = data['x']
#             tasks.append(fetch_elevation(session, lat, lon))
#
#         elevations = await asyncio.gather(*tasks)
#
#         for (node, data), elevation in zip(graph.nodes(data=True), elevations):
#             if elevation is not None:
#                 print("eleveation: ", elevation)
#                 graph.nodes[node]['elevation'] = elevation
#             else:
#                 graph.nodes[node]['elevation'] = 0
#
#     return graph


# def add_elevation_to_nodes(city_graph):
#     for node, data in city_graph.nodes(data=True):
#         lat = data['y']
#         lon = data['x']
#         elevation = get_elevation(lat, lon)
#         city_graph.nodes[node]['elevation'] = elevation
#     return city_graph

if __name__ == '__main__':
    g = get_graph_with_elevation_from_local("Jerusalem")
    print("hh")
    with open('elevation_dict.pkl', 'rb') as handle:
        data = pickle.load(handle)
        for u, v, key, data in g.edges(data=True, keys=True):
            print(data['height_diff'])