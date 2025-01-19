import osmnx as ox
import networkx as nx
import requests

def get_traffic_lights_count(start_address, end_address):
    # Get latitude and longitude for the start and end addresses
    start_location = ox.geocode(start_address)
    end_location = ox.geocode(end_address)

    # Get the OSM graph for the area with a smaller distance
    G = ox.graph_from_point(start_location, dist=5000, network_type='all')

    # Find the nearest nodes in the graph to the start and end locations
    start_node = ox.nearest_nodes(G, start_location[1], start_location[0])
    end_node = ox.nearest_nodes(G, end_location[1], end_location[0])

    # Find the shortest path between start and end nodes
    route = nx.shortest_path(G, start_node, end_node, weight="length")

    # Get the route as a list of coordinates
    route_coordinates = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]

    # Convert route coordinates to a bounding box for querying traffic lights
    min_lat = min(coord[0] for coord in route_coordinates)
    max_lat = max(coord[0] for coord in route_coordinates)
    min_lon = min(coord[1] for coord in route_coordinates)
    max_lon = max(coord[1] for coord in route_coordinates)

    # Query traffic lights using Overpass API
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node["highway"="traffic_signals"]
    ({min_lat},{min_lon},{max_lat},{max_lon});
    out count;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    data = response.json()

    # Return the count of traffic lights
    return data['elements'][0]['tags']['total']

# Example usage
start_address = "1600 Amphitheatre Parkway, Mountain View, CA"
end_address = "1 Infinite Loop, Cupertino, CA"
print(get_traffic_lights_count(start_address, end_address))