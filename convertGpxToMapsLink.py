import gpxpy


#we want to take the coordinates from the gpx file and generate a google maps link
#to do this we need to parse the gpx file and then generate the link
def parse_gpx(file_path):
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
    # base_url = "https://www.google.com/maps/dir/?api=1&travelmode=bicycling"
    path = "/".join([f"{lat},{lon}" for lat, lon in coordinates])
    return f"{base_url}{path}"


def get_google_maps_link(file_path):
    coord = parse_gpx(file_path)
    maps_url = generate_google_maps_url(coord)
    return maps_url

if __name__ == '__main__':
    file_path = "shortest_path.gpx"  # Replace with your GPX file path
    coordinates = parse_gpx(file_path)
    google_maps_url = generate_google_maps_url(coordinates)
    print("Google Maps URL:", google_maps_url)