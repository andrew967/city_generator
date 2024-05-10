import networkx as nx
from shapely.geometry import LineString


def find_shortest_path(polygons, bordered_polygons, riverpoint1, riverpoint2):
    G = nx.Graph()
    all_polygons = polygons + bordered_polygons

    for polygon in all_polygons:
        points = list(polygon.exterior.coords)
        for i in range(len(points) - 1):
            G.add_edge(points[i], points[i + 1], weight=LineString([points[i], points[i + 1]]).length)

    return nx.shortest_path(G, source=riverpoint1, target=riverpoint2, weight='weight')
