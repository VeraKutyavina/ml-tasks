import pygame
import copy
import random
import numpy as np
import pandas as pd
from pygame import QUIT

PINK = (255, 186, 211)

GREEN = (23, 151, 39)
YELLOW = (236, 200, 78)
RED = (218, 70, 47)

screen = pygame.display.set_mode((500, 500))
minPts = 3
minRadius = 50
COLORS = {
    'GREEN': GREEN,
    'YELLOW': YELLOW,
    'RED': RED,
}


def draw_circle(screen, x, y, color=PINK):
    pygame.draw.circle(screen, color, (x, y), 5)


def draw_flags(circles, flags):
    for j in range(len(circles)):
        draw_circle(screen, circles[j][0], circles[j][1], flags[j])

    pygame.display.flip()


def draw_clusters(cluster_df):
    for clust in np.unique(cluster):
        current_color = tuple(np.random.random(size=3) * 256)
        for k in range(len(cluster_df['cluster'])):
            if cluster_df['cluster'][k] == clust:
                draw_circle(screen, cluster_df["idx"][k][0], cluster_df["idx"][k][1], current_color)

    pygame.display.flip()


def dist(pntA, pntB):
    return np.sqrt((pntA[0] - pntB[0]) ** 2 + (pntA[1] - pntB[1]) ** 2)


def get_color(data, index, is_yellow_check=False):
    el_neighbours = []

    for i in range(len(data)):
        if i == index:
            continue
        if dist(data[index], data[i]) < minRadius:
            el_neighbours.append(i)

    if len(el_neighbours) >= minPts:
        return [COLORS['GREEN'], el_neighbours]

    elif (len(el_neighbours) < minPts) and len(el_neighbours) > 0:
        if is_yellow_check:
            return [COLORS['YELLOW'], el_neighbours]
        for j in range(len(el_neighbours)):
            color = get_color(data, el_neighbours[j], True)
            if color[0] == COLORS['GREEN']:
                return [COLORS['YELLOW'], el_neighbours]
        return [COLORS['RED'], el_neighbours]

    elif len(el_neighbours) == 0:
        return [COLORS['RED'], el_neighbours]


def get_cluster(data, flag, neighbour):
    k = 1

    current_points = []
    unvisited = copy.deepcopy(data)
    clusters = []

    while len(unvisited) != 0:
        first_point = True
        current_points.append(random.choice(unvisited))

        while len(current_points) != 0:

            el = current_points.pop(0)
            index = data.index(el)

            current_color = flag[index]
            current_neighbours = neighbour[index]

            unvisited.remove(el)

            unvisited_neighbours = []
            for j in current_neighbours:
                if data[j] in unvisited:
                    unvisited_neighbours.append(data[j])

            is_green = current_color == COLORS['GREEN']
            is_yellow = current_color == COLORS['YELLOW']
            is_red = current_color == COLORS['RED']

            if is_green:
                first_point = False

                clusters.append((el, k))
                element_neighbours = []
                for j in unvisited_neighbours:
                    if j not in current_points:
                        element_neighbours.append(j)

                current_points += element_neighbours

            elif is_yellow:
                clusters.append((el, k))

                continue

            elif is_red:
                clusters.append((el, 0))

                continue

        if not first_point:
            k += 1

    return clusters


if __name__ == '__main__':
    points = []
    flags = []
    neighbours = []

    is_running = True
    points = []
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    for i in range(len(points)):
                        res = get_color(points, i)
                        flags.append(res[0])
                        neighbours.append(res[1])

                    draw_flags(points, flags)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    clst = get_cluster(points, flags, neighbours)

                    idx, cluster = list(zip(*clst))
                    cluster_df = pd.DataFrame(clst, columns=["idx", "cluster"])

                    draw_clusters(cluster_df)

            if event.type == pygame.MOUSEBUTTONDOWN:
                (x, y) = pygame.mouse.get_pos()
                points.append([x, y])
                draw_circle(screen, x, y)
            pygame.display.flip()

            if event.type == QUIT:
                pygame.quit()
