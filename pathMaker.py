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


def get_node_from_coord(city_graph, coord):
    lat = coord[0]
    lon = coord[1]
    node = ox.nearest_nodes(city_graph, lon, lat)
    return node

def get_node_from_address(city_graph, city, street, number):
    point = ox.geocode(f"{street} {number}, {city}")
    node = ox.nearest_nodes(city_graph, point[1], point[0])
    return node


def get_circular_path(city_graph, origin, distance):
    #we want to find path with X length and return the url
    #this func will use the shortest path func and will return the  circular path
    #we want now to find 4 nodes.
    #origin, node1, node2, node3, destination=origin
    #we want to find node in distance/4 from the origin and than from node1 to node2 and so on

    pass



def run_test():
    city_graph = graph_builder.get_city_graph()
    origin = city_graph.nodes[0]
    destination = city_graph.nodes[1]
    best_path = get_shortest_path(city_graph, origin, destination)
    return best_path

if __name__ == '__main__':
    city = "Jerusalem"
    street = "King George"
    number = 20
    city_graph = graph_builder.get_city_graph()
    origin = get_node_from_address(city_graph, city, street, number)
    print(origin)