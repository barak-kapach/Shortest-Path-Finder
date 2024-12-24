from fiona.rfc3339 import pattern_time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from networkx import number_of_cliques

import app

"""
This is the main file of the project.
It contains the Flask server that will be used to communicate with the front-end.
"""
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Welcome to the Route Finder"

@app.route("/shortest", methods=['POST'])
def shortestPath():
    """
    This function will find the shortest path between two points in a city
    :return: the Google Maps link of the shortest path
    """
    # get the data from the request
    data = request.get_json()
    start_coords = data.get('currentLocation')
    country = data.get('country')
    city = data.get('city')
    street = data.get('street')
    number = data.get('number')
    hills = data.get('hills')

    # convert the string to a tuple
    start_coords = tuple(map(float, start_coords.split(',')))
    print("run run run ")
    maps_link = appli.find_short_path(start_coords, street, number, city, country, int(hills))

    # send the Google Maps link
    return jsonify({"maps_link": maps_link})


@app.route("/circular", methods=['POST'])
def circularPath():
    """
    This function will generate a circular route in a city
    :return: the Google Maps link of the circular route
    """
    # get the data from the request
    data = request.get_json()
    country = data.get('country')
    city = data.get('city')
    street = data.get('street')
    number = data.get('number')
    distance = data.get('distance')
    hills = data.get('hills')

    # run the circular route function
    maps_link = appli.generate_circular_route(street, number, city, country, float(distance), int(hills))
    print(maps_link)

    # send the Google Maps link
    return jsonify({"maps_link": maps_link})


if __name__ == '__main__':
    app.run()
