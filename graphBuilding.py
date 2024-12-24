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
    """
    this function will add the height difference to the edges of the graph
    :param city_graph: the city graph
    :return: the city graph with the height difference
    """
    for u, v, key, data in city_graph.edges(data=True, keys=True):
        elev_v = city_graph.nodes[v]['elevation']
        elev_u = city_graph.nodes[u]['elevation']
        data['height_diff'] = elev_v - elev_u
    return city_graph


def bike_weight_func(u, v, data, hills_factor=1):
    """
    this function will calculate the weight of the edge based on the length and the height difference
    :param u: node u
    :param v: node v
    :param data: data of the edge
    :param hills_factor: the factor of the hills
    :return: the weight of the edge
    """
    # get the length
    length = data.get('length', 1)
    # we already have the height difference, we want to give it a weight
    height_diff = data.get('height_diff', 0)
    if height_diff > 0:
        # going up
        data['weight'] = length + height_diff ** hills_factor
    else:
        # going down
        data['weight'] = max(1, abs(length + (height_diff * 2 * hills_factor)))  # (height * 2) is a negative number

    return data['weight']


def add_weight_to_the_graph(city_graph, weight_func, hills_factor=1):
    """
    this function will add the weight to the edges of the graph
    :param city_graph: city graph
    :param weight_func: the function that calculate the weight
    :param hills_factor: the factor of the hills
    :return: the graph with the weight
    """
    for u, v, key, data in city_graph.edges(data=True, keys=True):
        data['weight'] = weight_func(u, v, data, hills_factor)
    return city_graph


def get_elevetion_from_osmnx(latitude, longitude):
    """
    this function will get the elevation from the osmnx
    :param latitude: latitude
    :param longitude: longitude
    :return: the elevation
    """
    url = f"https://api.opentopodata.org/v1/srtm90m?locations={latitude},{longitude}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json().get('results', [])
        if results:
            return results[0]['elevation']
    return None


def add_elevation_data_with_osmnx(graph):
    """
    this function will add the elevation data to the graph
    :param graph: the graph
    :return: the graph with the elevation data
    """
    # iterate over the nodes
    counter = 0
    for node, data in graph.nodes(data=True):
        latitude = data['y']
        longitude = data['x']
        elevation = get_elevetion_from_osmnx(latitude, longitude)
        print(counter, "elevation: ", elevation)
        counter += 1
        if elevation is not None:
            graph.nodes[node]['elevation'] = elevation
        else:
            graph.nodes[node]['elevation'] = 0
        # to avoid the limit of the api request -> "error": "Per-second rate limit exceeded for the free hosted API.
        time.sleep(1)
    return graph


def add_elevation_data_to_the_graph_with_local_elevation_dict(graph):
    """
    this function will add the elevation data to the graph with the local elevation dict
    :param graph: the graph
    :return: the graph with the elevation data
    """
    # load the pickle file
    with open("elevation_dict.pkl", "rb") as f:
        elevation_dict = pickle.load(f)
    lst_of_nodes_that_dont_have_elevation = []
    for node, data in graph.nodes(data=True):
        lat = data['y']
        lon = data['x']
        # check if the lat and lon are in the dict
        if lat in elevation_dict and lon in elevation_dict[lat]:
            elev = elevation_dict[lat][lon]
        else:
            lst_of_nodes_that_dont_have_elevation.append((lat, lon))
            elev = 0
        graph.nodes[node]['elevation'] = elev
    print("")
    print(lst_of_nodes_that_dont_have_elevation)
    print(len(lst_of_nodes_that_dont_have_elevation))
    return graph


def get_graph_with_elevation_from_local(city, slope_value=1):
    """
    this function will get the graph with the elevation data from the local elevation dict
    :param city: city name
    :param slope_value: the slope value
    :return: the graph with the elevation data
    """
    graph = ox.graph_from_place(city, network_type="bike")
    print("Got the graph")
    graph = add_elevation_data_to_the_graph_with_local_elevation_dict(graph)
    print("Added the elevation data")
    graph = add_height_diff_to_edges(graph)
    print("Added the height difference")
    graph = add_weight_to_the_graph(graph, bike_weight_func, slope_value)
    return graph


# if __name__ == '__main__':
#     g = get_graph_with_elevation_from_local("Jerusalem")
#     print("hh")
#     with open('elevation_dict.pkl', 'rb') as handle:
#         data = pickle.load(handle)
#         for u, v, key, data in g.edges(data=True, keys=True):
#             print(data['height_diff'])
