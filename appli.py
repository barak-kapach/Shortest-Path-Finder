
"""
in this file we will use the functions from the other files to create a gpx file with the shortest path.

"""

import osmnx as ox
import networkx as nx
import random as Random
from PIL.ImagePalette import random

import graphBuilding as graph_builder
import pathMaker as path_maker
import expotrPath as path_exporter
import uploadGpxToDrive
import uploadToDrive
import convertGpxToMapsLink
import json

import requests


def run():
    pass



if __name__ == '__main__':
    print("start")
    city_graph = graph_builder.get_city_graph()
    print("got the graph")
    origin = list(city_graph.nodes())[0]
    ind = len(list(city_graph.nodes()))
    #get random number between 1 and ind
    random_ind = Random.randint(0, ind)
    destination = list(city_graph.nodes())[random_ind]

    best_path = path_maker.get_shortest_path(city_graph, origin, destination)
    path_exporter.export_shortest_path_to_gpx(city_graph, best_path, "shortest_path.gpx")
    #show the path in plot
    ox.plot_graph_route(city_graph, best_path)
    print("done with the path")
    uploadToDrive.upload_to_drive("shortest_path")
    maps_link = convertGpxToMapsLink.get_google_maps_link("shortest_path.gpx")
    print("Google Maps URL:", maps_link)



    #
    # ###
    # headers = {
    #     "Authorization": "Bearer ya29.a0AeDClZBj0ltn_qIxNddL6HMZoflHf-sRL54gMl5gHQKpEj_igKtoxdjNmZnEGLhTBzTVhwn4M36u7dhNMdTZljJwpd4dwoyt17mR-F_LmFkEvjrTQKGzcPVimh_C7jRPeGLx9uc1cSc8_-iVsAQAMlyCmdjCkBZoy-Cyyhk4aCgYKATkSARESFQHGX2Mi0Ha24zGfDk0NmrxWBhUsYw0175"}
    # para = {"name": "shortestPath.gpx",
    #         "parents": ["1VrlTjWDOQx-NNMGdbYAf7DPVH4i_dKBq"]}
    #
    # files = {
    #     'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
    #     'file': ('application/gpx+xml', open("./shortest_path.gpx", 'rb'))
    # }
    #
    # r = requests.post(
    #     "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
    #     headers=headers,
    #     files=files
    # )

    ###