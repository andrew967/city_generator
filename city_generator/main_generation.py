import numpy as np
from scipy.spatial import Voronoi
from shapely.affinity import scale


from city_generator.geometry_utils import *
from city_generator.graph_utils import find_shortest_path
from city_generator.vizualization import vizualize


def generate_voronoi_diagramm(points):
    return Voronoi(points)

def main_generation(n):
    success = False
    while not success:
        try:
            points = np.random.rand(n, 2)
            vor = generate_voronoi_diagramm(points)
            polygons = find_all_inside_poligons(vor)
            bordered_polygons = find_all_outside_poligons(vor)
            riverpoint1, riverpoint2 = init_river(bordered_polygons)
            path = find_shortest_path(polygons,bordered_polygons, riverpoint1, riverpoint2)
            multi_polygon = ops.unary_union(polygons)
            scaled_polygons = [scale(poly, 0.8, 0.8, origin='center') for poly in polygons]
            divided_polygons = []

            fig = vizualize(scaled_polygons, multi_polygon, divided_polygons, path, riverpoint1, riverpoint2)

            success = True
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
    return fig
