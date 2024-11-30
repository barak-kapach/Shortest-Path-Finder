import gpxpy


# we want to take the coordinates from the gpx file and generate a google maps link
# to do this we need to parse the gpx file and then generate the link
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
    base_url = "https://www.google.com/maps/dir/"
    path = "/".join([f"{lat},{lon}" for lat, lon in coordinates])
    return f"{base_url}{path}"


def get_google_maps_link(file_path):
    coord = parse_gpx(file_path)
    maps_url = generate_google_maps_url(coord)
    return maps_url
