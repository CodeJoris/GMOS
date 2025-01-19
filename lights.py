import osmnx as ox
import networkx as nx
import time
import math


def haversine(coord1, coord2):
    # Coordinates in decimal degrees (e.g. 43.60, -79.49)
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r * 1000  # Return value will be in meters


def count_crossing_spots(start_address, end_address):
    # Get latitude and longitude for the start and end addresses
    start_location = ox.geocode(start_address)
    end_location = ox.geocode(end_address)

    distance = haversine(start_location, end_location)

    # Get the OSM graph for the area
    G = ox.graph_from_point(start_location, dist=distance, network_type='drive')

    # Find the nearest nodes in the graph to the start and end locations
    start_node = ox.nearest_nodes(G, start_location[1], start_location[0])
    end_node = ox.nearest_nodes(G, end_location[1], end_location[0])

    # Find the shortest path between start and end nodes
    route = nx.shortest_path(G, start_node, end_node, weight="length")

    # Count crossing spots (nodes with 3 or more neighbors) along the route
    crossing_spots_count = 0
    for node in route:
        if len(list(G.neighbors(node))) >= 3:
            crossing_spots_count += 1

    return crossing_spots_count

# Example usage
# start_address = "Trottier Building, Montreal, Quebec, Canada"
# end_address = "5633 Rue Plantagenet, Montreal, Quebec, Canada"
# a=time.time()
# crossing_spots = count_crossing_spots(start_address, end_address)
# print(time.time() - a)

# print(f"Number of crossing spots along the route: {crossing_spots}")
