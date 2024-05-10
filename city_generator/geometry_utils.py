import random
import shapely.ops as ops
from shapely.geometry import Polygon, LineString, GeometryCollection

x_min, x_max = 0, 1
y_min, y_max = 0, 1

def find_closest_point_on_border(x, y):
    distances = {
        (0, y): x,
        (1, y): 1 - x,
        (x, 0): y,
        (x, 1): 1 - y
    }
    closest_point = min(distances, key=distances.get)

    return closest_point


def split_polygon(polygon, depth=1):
    minx, miny, maxx, maxy = polygon.bounds
    width = maxx - minx
    height = maxy - miny
    horizontal = width < height

    if horizontal:
        splitter = LineString([(minx, (miny + maxy) / 2), (maxx, (miny + maxy) / 2)])
    else:
        splitter = LineString([((minx + maxx) / 2, miny), ((minx + maxx) / 2, maxy)])

    splitted = ops.split(polygon, splitter)
    if isinstance(splitted, GeometryCollection):
        parts = [geom for geom in splitted.geoms if isinstance(geom, Polygon)]
    else:
        parts = [splitted]

    if depth > 1:
        new_parts = []
        for part in parts:
            new_parts.extend(split_polygon(part, depth - 1))
        return new_parts
    return parts

def get_edge_points(vertices):
    edge_points = []
    for vertex in vertices:
        x, y = vertex
        if x == x_min or x == x_max or y == y_min or y == y_max:
            edge_points.append(vertex)
    return edge_points


def get_border_line(poly):
    x, y = poly.exterior.xy
    return LineString(list(zip(x, y)))

def find_nearest_point(line, polygon):
    centroid = polygon.centroid
    return line.interpolate(line.project(centroid))

def init_depth(area):
    if area > 0.03:
        depth = 5
    elif area > 0.02:
        depth = 4
    elif area > 0.01:
        depth = 3
    elif area > 0.005:
        depth = 3
    else:
        depth = 1
    return depth

def find_all_inside_poligons(vor):
    polygons = []

    for region_index in vor.point_region:
        region = vor.regions[region_index]
        if -1 in region:
            continue
        polygon = [vor.vertices[i] for i in region]
        if all(x_min <= x <= x_max and y_min <= y <= y_max for x, y in polygon):
            polygons.append(Polygon(polygon))
    return polygons

def find_all_outside_poligons(vor):
    bordered_polygons = []

    def is_inside(x, y):
        return x_min <= x <= x_max and y_min <= y <= y_max

    for region_index in vor.point_region:
        vertices = vor.regions[region_index]
        if -1 in vertices:
            continue

        polygon = [vor.vertices[i] for i in vertices]
        fully_inside = all(is_inside(x, y) for x, y in polygon)

        if not fully_inside:
            touches_border = any(x <= x_min or x >= x_max or y <= y_min or y >= y_max for x, y in polygon)
            if touches_border:
                bordered_polygons.append(Polygon(polygon))
    return bordered_polygons


def init_river(bordered_polygons):
    riverpoint1 = random.choice(list(random.choice(bordered_polygons).exterior.coords))
    riverpoint2 = random.choice(list(random.choice(bordered_polygons).exterior.coords))
    while True:
        if riverpoint1 == riverpoint2:
            riverpoint2 = random.choice(list(random.choice(bordered_polygons).exterior.coords))
        break
    riverpoint1, riverpoint2 = find_river_points(bordered_polygons, riverpoint1, riverpoint2)
    return riverpoint1, riverpoint2

def find_river_points(bordered_polygons, riverpoint1, riverpoint2):
    all_edge_points = []
    for polygon in bordered_polygons:
        edge_points = get_edge_points(polygon.exterior.coords)
        all_edge_points.extend(edge_points)

    if len(all_edge_points) > 1:
        riverpoint1 = random.choice(all_edge_points)
        riverpoint2 = random.choice(all_edge_points)
        while riverpoint2 == riverpoint1:
            riverpoint2 = random.choice(all_edge_points)
    if not (0 <= riverpoint1[0] <= 1 and 0 <= riverpoint1[1] <= 1 and 0 <= riverpoint2[0] <= 1 and 0 <=
            riverpoint2[1] <= 1):
        raise ValueError("Points are outside of the designated area.")
    return riverpoint1, riverpoint2
