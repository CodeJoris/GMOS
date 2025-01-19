import osmnx as ox
import networkx as nx

def count_crossing_spots(start_address, end_address):
    # Get latitude and longitude for the start and end addresses
    start_location = ox.geocode(start_address)
    end_location = ox.geocode(end_address)

    # Get the OSM graph for the area
    G = ox.graph_from_point(start_location, dist=10000, network_type='drive')

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
start_address = "5633 rue plantagenet, Montreal, Quebec, Canada"
end_address = "4917 rue fulton, Montreal, Quebec, Canada"
crossing_spots = count_crossing_spots(start_address, end_address)

print(f"Number of crossing spots along the route: {crossing_spots}")
