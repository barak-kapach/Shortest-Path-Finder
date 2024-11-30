# from flask import Flask, request, jsonify, render_template_string
# from flask_cors import CORS
# import appli
#
# app = Flask(__name__)
# CORS(app)
#
# @app.route("/")
# def home():
#     return render_template_string('''
#         <h1>Welcome to the Route Finder</h1>
#         <a href="/shortest">Find Shortest Path</a><br>
#         <a href="/circular">Create Circular Path</a>
#     ''')
#
# @app.route("/shortest", methods=['GET', 'POST'])
# def shortestPath():
#     if request.method == 'POST':
#         data = request.get_json()
#         start_coords = data.get('currentLocation')
#         country = data.get('country')
#         city = data.get('city')
#         street = data.get('street')
#         number = data.get('number')
#         hills = data.get('hills')
#         start_coords = tuple(map(float, start_coords.split(',')))
#         maps_link = appli.find_short_path(start_coords, street, number, city, country, hills)
#         return jsonify({"maps_link": maps_link})
#     return render_template_string('''
#         <h1>Find Shortest Path</h1>
#         <!-- Add your form here to collect data for the shortest path -->
#     ''')
#
# @app.route("/circular", methods=['GET', 'POST'])
# def circularPath():
#     data = request.get_json()
#     country = data.get('country')
#     city = data.get('city')
#     street = data.get('street')
#     number = data.get('number')
#     distance = data.get('distance')
#     hills = data.get('hills')
#     maps_link = appli.generate_circular_route(street, number, city, country, distance)
#     return jsonify({"maps_link": maps_link})
#
#
# if __name__ == '__main__':
#     app.run()
#
# import pickle
#
# if __name__ == '__main__':
#     #we want to load the dict from the pickle file
#     with open('elevation_dict.pkl', 'rb') as handle:
#         data = pickle.load(handle)
#     print(len(data))