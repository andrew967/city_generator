from city_generator.geometry_utils import *

import matplotlib.pyplot as plt
import numpy as np
import shapely.ops as ops
from shapely.geometry import LineString
from shapely.affinity import scale


def draw_castle_or_district(ax, scaled_polygons, multi_polygon, divided_polygons):
    Castle = False
    for poly in scaled_polygons:
        area = poly.area
        if area > 0.02 and not Castle:
            Castle = True
            draw_castle_with_moat(ax, poly, multi_polygon)
        else:
            depth = init_depth(area)
            parts = split_polygon(poly, depth)
            divided_polygons.extend(parts)

    color_divided_polygons(ax, divided_polygons, scaled_polygons)


def draw_castle_with_moat(ax, poly, multi_polygon):
    castle_border = scale(poly, 0.9, 0.9)
    open_line = get_border_line(castle_border)
    nearest_point = find_nearest_point(open_line, multi_polygon)
    draw_moat(ax, open_line, nearest_point)
    draw_central_square(ax, castle_border)


def draw_moat(ax, line, nearest_point):
    cut_length = 0.1
    nearest_point_dist = line.project(nearest_point)
    cut_start = max(0, nearest_point_dist - cut_length / 2)
    cut_end = min(line.length, nearest_point_dist + cut_length / 2)
    remaining_line_part1 = ops.substring(line, 0, cut_start)
    remaining_line_part2 = ops.substring(line, cut_end, line.length)

    ax.plot(*remaining_line_part1.xy, 'black', linewidth=3)
    ax.plot(*remaining_line_part2.xy, 'black', linewidth=3)

    cut_start_point = line.interpolate(cut_start)
    cut_end_point = line.interpolate(cut_end)
    ax.plot([cut_start_point.x, cut_end_point.x], [cut_start_point.y, cut_end_point.y], 'ko', markersize=7)


def draw_central_square(ax, poly):
    centroid = poly.centroid
    square_size = 0.1
    square_coords = [
        (centroid.x - square_size / 4, centroid.y - square_size / 4),
        (centroid.x + square_size / 4, centroid.y - square_size / 4),
        (centroid.x + square_size / 4, centroid.y + square_size / 4),
        (centroid.x - square_size / 4, centroid.y + square_size / 4),
        (centroid.x - square_size / 4, centroid.y - square_size / 4)
    ]
    square_x, square_y = zip(*square_coords)
    ax.fill(square_x, square_y, color="black")


def color_divided_polygons(ax, divided_polygons, scaled_polygons):
    for poly in divided_polygons:
        x, y = poly.exterior.xy
        for par in scaled_polygons:
            if poly.intersects(par.exterior.buffer(0.001)):
                ax.fill(x, y, alpha=0.7, color="grey", edgecolor='black')
                break


def draw_river(ax, path, riverpoint1, riverpoint2):
    path_line = LineString(path)
    x, y = path_line.xy
    ax.plot(x, y, color='blue', linewidth=6.5)

    point = find_closest_point_on_border(riverpoint1[0], riverpoint1[1])
    x = [riverpoint1[0], point[0]]
    y = [riverpoint1[1], point[1]]
    ax.plot(x, y, color='blue', linewidth=6.5)

    point = find_closest_point_on_border(riverpoint2[0], riverpoint2[1])
    x = [riverpoint2[0], point[0]]
    y = [riverpoint2[1], point[1]]
    ax.plot(x, y, color='blue', linewidth=6.5)
    draw_bridges(ax, path_line)


def draw_bridges(ax, path_line):
    path_length = path_line.length
    bridge_positions = [path_line.interpolate(path_length * i / 4) for i in range(1, 4)]

    for bridge in bridge_positions:
        bridge_x, bridge_y = bridge.x, bridge.y
        bridge_size = 0.015
        ax.plot([bridge_x - bridge_size, bridge_x + bridge_size], [bridge_y, bridge_y], color='black',
                linewidth=5)


def draw_walls(ax, multi_polygon):
    exterior = multi_polygon.exterior
    vertices = np.array(exterior.coords)
    ax.plot(*exterior.xy, color='black', linewidth=3)
    ax.plot(vertices[:, 0], vertices[:, 1], 'ko', markersize=6.5)


def vizualize(scaled_polygons, multi_polygon, divided_polygons, path, riverpoint1, riverpoint2):
    fig, ax = plt.subplots()
    draw_castle_or_district(ax, scaled_polygons, multi_polygon, divided_polygons)
    draw_walls(ax, multi_polygon)
    draw_river(ax, path, riverpoint1, riverpoint2)
    return fig
