import gpxpy
import gpxpy.gpx

"""
   in this file we will create a gpx file with the shortest path. 
"""

def export_shortest_path_to_gpx(city_graph, best_path, output_file):
    # create a gpx object
    gpx = gpxpy.gpx.GPX()

    # create a track
    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)

    # create a segment
    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)

    # add points to the segment
    for node in best_path:
        node_data = city_graph.nodes[node]
        point = gpxpy.gpx.GPXTrackPoint(node_data['y'], node_data['x'])
        segment.points.append(point)

    # write the gpx file
    with open(output_file, "w") as f:
        f.write(gpx.to_xml())
    print("done  with export!")