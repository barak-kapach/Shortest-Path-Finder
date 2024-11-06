import expotrPath
import graphBuilding
import osmnx as ox
import networkx as nx
import convertGpxToMapsLink

def length_of_path(graph, path):
    start_node = path[0]
    end_node = path[-1]
    length = nx.shortest_path_length(graph, start_node, end_node, weight='length')
    return length


def find_circular_routes(graph, start_node, path_length, max_depth=30):
    """

    :param graph: city graph
    :param start_node: origin node of the path
    :param path_length: the length of the path in KM
    :param max_depth: the max depth of the path - how many nodes we want to visit
    :return:
    """
    def dfs(cur_node, path, visited):
        if len(path) > 1 and cur_node == start_node:
            # filter the path that are not in the relevant length
            if length_of_path(graph, path) > path_length + 0.5:
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


def calculate_grade_of_circular_route(city_graph, path, weight='weight'):
    # iin this func we need to get the relevant weight of the path
    grade = 0
    for i in range(len(path) - 1):
        u = path[i]
        v = path[i + 1]
        data = city_graph.get_edge_data(u, v)
        grade += data['length']
    return grade


def find_best_circular_route_from_circular_route_list(graph, circular_routes):
    best_path = None
    # create max num for best grade
    best_path_grade = float('inf')
    for route in circular_routes:
        cur_grade = calculate_grade_of_circular_route(graph, route)
        if best_path_grade > cur_grade:
            best_path_grade = cur_grade
            best_path = route
    return best_path


def find_best_circular_route(city_graph, start_node, path_length):
    circular_routes = find_circular_routes(city_graph, start_node, path_length)
    # best_path = find_best_circular_route_from_circular_route_list(city_graph, circular_routes)
    # return best_path
    return circular_routes

if __name__ == '__main__':
    city_graph = graphBuilding.get_city_graph()
    start_node = list(city_graph.nodes())[0]
    best_path = find_best_circular_route(city_graph, start_node, 15)
    bs = find_best_circular_route_from_circular_route_list(city_graph, best_path)
    print(bs)
    # print(best_path)
    # ox.plot_graph_route(city_graph, best_path)
    # path= best_path[0]
    # for i in range(len(path)):
    #     if len(path) < len(best_path[i]):
    #         print(path)
    #         path = best_path[i]
    # ox.plot_graph_route(city_graph, path,dpi=1000)
    # expotrPath.export_shortest_path_to_gpx(city_graph,path,"shortest_path.gpx")
    # print(convertGpxToMapsLink.get_google_maps_link("shortest_path.gpx"))

