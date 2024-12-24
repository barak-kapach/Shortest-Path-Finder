import expotrPath
import graphBuilding
import osmnx as ox
import convertGpxToMapsLink
import networkx as nx

"""
this file is responsible for creating circular routes in the city
"""


def length_of_path(graph, path):
    """
    This function will return the length of the path in meters
    :param graph: osmnx graph
    :param path: list of nodes
    :return: the length of the path in meters
    """
    start_node = path[0]
    end_node = path[-1]
    length = nx.shortest_path_length(graph, start_node, end_node, weight='length')
    return length


def find_circular_routes(graph, start_node, path_length, max_depth=50):
    """
    This function will find all the circular routes in the city
    :param graph: city graph
    :param start_node: origin node of the path
    :param path_length: the length of the path in KM
    :param max_depth: the max depth of the path - how many nodes we want to visit
    :return:
    """

    def dfs(cur_node, path, visited):
        if len(path) > 2 and cur_node == start_node:
            # filter the path that are not in the relevant length
            # path length is the length of the path in KM and the function return the length of the path in meters
            if length_of_path(graph, path) > (path_length + path_length * 0.5) * 1000:
                print("length_of_path(graph, path)-->> bigger ", str(length_of_path(graph, path)))
                return
            circular_paths.append(path[:])
            return
        if len(path) > max_depth:
            return
        for neighbor in graph.neighbors(cur_node):
            if neighbor not in visited or (neighbor == start_node and len(path) > 1):
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor, path, visited)
                path.pop()
                visited.remove(neighbor)

    circular_paths = []
    dfs(start_node, [start_node], {start_node})
    return circular_paths


def calculate_grade_of_circular_route(city_graph, path, weight='length'):
    """
    This function will calculate the grade of the path
    :param city_graph: osmnx graph
    :param path: list of nodes
    :param weight: the weight of the path
    :return: the grade of the path
    """
    # In this function, we need to get the relevant weight of the path
    grade = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        try:
            length = nx.shortest_path_length(city_graph, u, v, weight=weight)
            grade += length
        except nx.NetworkXNoPath:
            print(f"No path between {u} and {v}")
    return grade


def find_best_circular_route_from_circular_route_list(graph, circular_routes, length, weight='length'):
    """
    This function will find the best circular route from the list of circular routes
    :param graph: osmnx graph
    :param circular_routes: list of circular routes
    :param length: the length of the path in KM
    :param weight: the weight of the path
    :return: the best circular route
    """
    path = None
    # create max num for best grade
    best_path_grade = 0
    for route in circular_routes:
        cur_grade = calculate_grade_of_circular_route(graph, route)
        # here we want to check which path closer to the length
        if abs(cur_grade - length * 1000) < abs(best_path_grade - length * 1000):
            print("cur_grade", str(cur_grade))
            best_path_grade = cur_grade
            path = route
    return path


def find_best_circular_route(city_graph, start_node, path_length):
    """
    This function will find the best circular route in the city
    :param city_graph: osmnx graph
    :param start_node: origin node of the path
    :param path_length: the length of the path in KM
    :return: the best circular route
    """
    circular_routes = find_circular_routes(city_graph, start_node, path_length)
    best_path = find_best_circular_route_from_circular_route_list(city_graph, circular_routes, path_length)
    return best_path

# if __name__ == '__main__':
#     #test
#     city_graph = graphBuilding.get_graph_with_elevation_from_local("Jerusalem", 1)
#     start_node = list(city_graph.nodes())[0]
#     best_path = find_best_circular_route(city_graph, start_node, 5)
#     print(best_path)
