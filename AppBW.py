# import osmnx as ox
# from osmnx import distance
# import networkx as nx
# import random as Random
# from PIL.ImagePalette import random
#
# import graphBuilding as graph_builder
# import pathMaker as path_maker
# import expotrPath as path_exporter
# import uploadGpxToDrive
# import uploadToDrive
# import convertGpxToMapsLink
# import json
# from geopy.geocoders import Nominatim
#
# import requests
#
#
# def get_coordinates_from_address(address):
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     location = geolocator.geocode(address)
#     if location:
#         return location.latitude, location.longitude
#     else:
#         raise ValueError("Address not found")
#
#
# def run(city, start_coords, address, slope_value):
#     print("run of the AppBW")
#     city_graph, nodes, edges = graph_builder.get_city_graph()
#     print("Got the graph")
#
#     # Convert address to coordinates
#     end_coords = get_coordinates_from_address(address)
#     print(f"End coordinates: {end_coords}")
#
#     # Find the nearest nodes to the coordinates
#     origin = ox.distance.nearest_nodes(city_graph, start_coords[1], start_coords[0])
#     destination = ox.distance.nearest_nodes(city_graph, end_coords[1], end_coords[0])
#
#     # Add elevation data to the graph
#     # TODO - add the api key of the google elevation api by query
#     city_graph = graph_builder.add_elevation_to_nodes(city_graph, "AIzaSyD-8Jk3Z1Q7Q7v4Q7Z2Q7v4Q7Z2Q7v4Q7Z2")
#
#     # Get the shortest path
#     best_path = path_maker.get_shortest_path(city_graph, origin, destination)
#     path_exporter.export_shortest_path_to_gpx(city_graph, best_path, "shortest_path.gpx")
#
#     # Show the path in plot
#     ox.plot_graph_route(city_graph, best_path)
#     print("Done with the path")
#
#     # Convert GPX to Google Maps link
#     maps_link = convertGpxToMapsLink.get_google_maps_link("shortest_path.gpx")
#     print("Google Maps URL:", maps_link)
