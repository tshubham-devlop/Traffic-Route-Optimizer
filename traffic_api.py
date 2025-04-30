# traffic_api.py

import osmnx as ox

def fetch_traffic_data(bbox):
    """
    Fetches road network from OpenStreetMap within the given bounding box.

    Parameters:
    bbox (list or tuple): [south, west, north, east]

    Returns:
    GeoDataFrame: GeoDataFrame of road network edges
    """
    south, west, north, east = bbox

    # For osmnx==1.5.1, this function is available directly
    G = ox.graph_from_bbox(
        north=north,
        south=south,
        east=east,
        west=west,
        network_type='drive'
    )

    # Convert to GeoDataFrame of edges (roads)
    gdf_edges = ox.graph_to_gdfs(G, nodes=False, edges=True)

    return gdf_edges
