from fiona.rfc3339 import pattern_time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import appli
import circularRouteMaker
import graphBuilding
from appli import generate_circular_route


app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Welcome to the Route Finder"

@app.route("/shortest", methods=['POST'])
def shortestPath():
    data = request.get_json()

    start_coords = data.get('currentLocation')
    country = data.get('country')
    city = data.get('city')
    street = data.get('street')
    number = data.get('number')
    hills = data.get('hills')
    start_coords = tuple(map(float, start_coords.split(',')))
    print("run run run ")
    maps_link = appli.find_short_path(start_coords, street, number, city, country, hills)

    #send the Google Maps link
    return jsonify({"maps_link": maps_link})


@app.route("/circular", methods=['POST'])
def circularPath():
    data = request.get_json()
    country = data.get('country')
    city = data.get('city')
    street = data.get('street')
    number = data.get('number')
    distance = data.get('distance')
    hills = data.get('hills')
    maps_link = appli.generate_circular_route(street, number, city, country, distance)
    print(maps_link)
    return jsonify({"maps_link": maps_link})

if __name__ == '__main__':
    app.run()