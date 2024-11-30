"""
in this file we will use the functions from the other files to create a gpx file with the shortest path.

"""
# import networkx as nx
# import random as Random
# import json
# import uploadGpxToDrive
# import uploadToDrive
# import requests
import osmnx as ox
from osmnx import distance

import graphBuilding
import pathMaker
import circularRouteMaker
import expotrPath
import convertGpxToMapsLink
from geopy.geocoders import Nominatim




def address_to_coordinates(street, number, city, country):
    """
    This function will convert an address to coordinates
    :return: return the coordinates of the address in the format (latitude, longitude)
    """
    # Combine the address parts into a single string
    address = f"{number} {street}, {city}, {country}"

    # Initialize the geolocator
    geolocator = Nominatim(user_agent="route_finder_app")

    # Use the geolocator to get location data
    location = geolocator.geocode(address)

    # If the location was found, return the coordinates else return None
    if location:
        return location.latitude, location.longitude
    else:
        return None

def find_short_path(start_coords, street, number, city, country, slope_value):
    """
    This function will find the shortest path between two points in a city
    :param start_coords: origin coordinates
    :param slope_value:  represent the slope value that the user want to avoid
    :return:
    """
    #initialize the graph
    city_name = f"{city}, {country}"

    city_graph = graphBuilding.get_graph_with_elevation_from_local(city_name, slope_value)
    print("Got the graph")

    # Convert address to coordinates
    end_coords = address_to_coordinates(street, number, city, country)

    # Find the nearest nodes to the coordinates
    origin = ox.nearest_nodes(city_graph, start_coords[1], start_coords[0])
    destination = ox.nearest_nodes(city_graph, end_coords[1], end_coords[0])

    # Get the shortest path
    best_path = pathMaker.get_shortest_path(city_graph, origin, destination)
    expotrPath.export_shortest_path_to_gpx(city_graph, best_path, "shortest_path.gpx")

    print("Done with the path - run function")

    # Convert GPX to Google Maps link
    maps_link = convertGpxToMapsLink.get_google_maps_link("shortest_path.gpx")
    print("Google Maps URL:", maps_link)
    return maps_link



def generate_circular_route(street, number, city, country, path_length, hills):
    # Get the city graph
    city_name = f"{city}, {country}"
    city_graph= graphBuilding.get_graph_with_elevation_from_local(city_name, hills)

    # Get the start coordinates from the address
    start_coords = address_to_coordinates(street, number, city, country)

    # Get the start node
    start_node = ox.distance.nearest_nodes(city_graph, start_coords[1], start_coords[0])

    # Find the best circular route
    best_path = circularRouteMaker.find_best_circular_route(city_graph, start_node, path_length)

    # Export the circular route to a GPX file
    expotrPath.export_shortest_path_to_gpx(city_graph, best_path, "shortest_path.gpx")

    # Convert the GPX file to a Google Maps link
    maps_link = convertGpxToMapsLink.get_google_maps_link("shortest_path.gpx")

    return maps_link
