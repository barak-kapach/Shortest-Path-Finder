import osmnx as ox

"""
    in this file we create a weight function and find the shortest path.
"""


def get_shortest_path(city_graph, origin, destination, weight='weight'):
    # use the shortest path function from osmnx
    shortest_path = ox.shortest_path(city_graph, origin, destination, weight)
    return shortest_path


# find the k shortest paths
def get_k_shortest_paths(city_graph, origin, destination, k, weight='weight'):
    # use the k_shortest_paths function from osmnx
    k_shortest_paths = ox.k_shortest_paths(city_graph, origin, destination, k, weight)
    return k_shortest_paths


def get_node_from_coord(city_graph, coord):
    """
    get the nearest node to the given coordinates
    :param city_graph: city graph object - osmnx graph
    :param coord: lat, lon coordinates
    :return: nearest node of the given coordinates
    """
    lat = coord[0]
    lon = coord[1]
    node = ox.nearest_nodes(city_graph, lon, lat)
    return node


def get_node_from_address(city_graph, city, street, number):
    """
    get the nearest node to the given address
    :param city_graph: city graph object - osmnx graph
    :param city: city name - string
    :param street: street name - string
    :param number: number of the house - int
    :return: nearest node of the given address
    """
    point = ox.geocode(f"{street} {number}, {city}")
    node = ox.nearest_nodes(city_graph, point[1], point[0])
    return node
