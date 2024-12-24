import gpxpy

"""
This script takes a GPX file and generates a Google Maps link from the coordinates in the file.
"""


def parse_gpx(file_path):
    """
    Parse a GPX file and return the coordinates
    :param file_path: path to the GPX file
    :return: list of coordinates - represented as tuples of (latitude, longitude)
    """
    with open(file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        coordinates = []
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    coordinates.append((point.latitude, point.longitude))
    return coordinates


def generate_google_maps_url(coordinates):
    """
    Generate a Google Maps URL from a list of coordinates
    :param coordinates: list of coordinates - represented as tuples of (latitude, longitude)
    :return: Google Maps URL
    """
    base_url = "https://www.google.com/maps/dir/"
    path = "/".join([f"{lat},{lon}" for lat, lon in coordinates])
    return f"{base_url}{path}"


def get_google_maps_link(file_path):
    """
    Generate a Google Maps link from a GPX file
    :param file_path: path to the GPX file
    :return: Google Maps URL
    """
    coord = parse_gpx(file_path)
    maps_url = generate_google_maps_url(coord)
    return maps_url
