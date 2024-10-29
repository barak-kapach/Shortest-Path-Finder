import osmnx as ox
import graphBuilding as graph_builder

"""
    in this file we create a weight function and find the shortest path.
"""


def get_shortest_path(city_graph, origin, destination):
    # use the shortest path function from osmnx
    shortest_path = ox.shortest_path(city_graph, origin, destination, weight='weight')
    return shortest_path


# find the k shortest paths
def get_k_shortest_paths(city_graph, origin, destination, k):
    #we can create some path base on different weight and give to the user best path base on something
    # use the k_shortest_paths function from osmnx
    k_shortest_paths = ox.k_shortest_paths(city_graph, origin, destination, k, weight='weight')
    return k_shortest_paths


def run_test():
    city_graph = graph_builder.get_city_graph()
    origin = city_graph.nodes[0]
    destination = city_graph.nodes[1]
    best_path = get_shortest_path(city_graph, origin, destination)
    return best_path
