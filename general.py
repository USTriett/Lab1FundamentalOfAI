

G_MAX = 10 ** 8
numNeibour = 4
adjX = [-1, 0, 1, 0]
adjY = [0, 1, 0, -1]

import os
from enum import Enum

from pip._internal.utils.misc import enum


def read_file(file_name: str = 'input1.txt'):
    # mo file
    f = open(file_name, 'r')

    # so diem thuong
    n_bonus_points = int(next(f)[:-1])

    # danh sach diem thuong: x y diem
    bonus_points = []
    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    # doc me cung
    text = f.read()
    matrix = [list(i) for i in text.splitlines()]
    f.close()

    # tra ve: danh sach diem thuong & me cung
    return bonus_points, matrix


def find_start(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    for i in range(numRows):
        for j in range(numCols):
            if matrix[i][j] == 'S':
                return i, j


def find_end(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    for i in range(numRows):
        if matrix[i][0] != 'x':
            return i, 0
        elif matrix[i][numCols - 1] != 'x':
            return i, numCols - 1

    for j in range(numCols):
        if matrix[0][j] != ' ':
            return 0, j
        elif matrix[numRows - 1][j] != 'x':
            return numRows - 1, j


def creatCostMatrix(matrix, bonus_points):
    switcher = {
        'x': G_MAX,
        ' ': 1,
        'S': 0,
        '+': -1,
        'G': 1,
        'T': 1
        # '+' khong quan trong vi se update sau
    }

    numRows = len(matrix)
    numCols = len(matrix[0])

    cost = [[switcher.get(matrix[i][j]) for j in range(numCols)] for i in range(numRows)]

    for i in range(len(bonus_points)):
        x = bonus_points[i][0]
        y = bonus_points[i][1]
        reward = bonus_points[i][2]
        cost[x][y] = reward

    return cost


def isInMatrix(matrix, x, y):
    if x < 0:
        return False
    if y < 0:
        return False
    if x >= len(matrix):
        return False
    if y >= len(matrix[0]):
        return False
    return True


def check(matrix, x, y):
    if (isInMatrix(matrix, x, y) == True):
        return (matrix[x][y] != 'x')
    return False


def trace(matrix, cost, costMatrix, start, end):
    route = [end]
    v = end
    while v != start:
        for i in range(numNeibour):
            x = v[0] - adjX[i]
            y = v[1] - adjY[i]
            if check(matrix, x, y) is True and cost[x][y] == cost[v[0]][v[1]] - costMatrix[v[0]][v[1]]:
                route.append((x, y))
                v = (x, y)
                break
    route.reverse()

    return cost[end[0]][end[1]], route


import astar
import bfs
import dfs
import greedy
import ucs
import teleport

class ALGORITHM_NAME(str, Enum):
    BFS = 'bfs'
    DFS = 'dfs'
    UCS = 'ucs'
    GREEDY = 'greedy',
    ASTAR = 'astar',
    TELE = 'teleport'

def get_func_dict(alg_name, d, start_pos, end_pos, costMatrix, myMaze, *args):
    # print(alg_name)
    if alg_name == ALGORITHM_NAME.BFS:
        return bfs.bfs(d, start_pos, end_pos, costMatrix, myMaze)
    elif alg_name == ALGORITHM_NAME.DFS:
        return dfs.dfs(d, start_pos, end_pos, costMatrix, myMaze)
    elif alg_name == ALGORITHM_NAME.UCS:
        return ucs.ucs(d, start_pos, end_pos, costMatrix, myMaze)
    elif alg_name == ALGORITHM_NAME.GREEDY:
        return greedy.greedy(d, start_pos, end_pos, costMatrix, myMaze)
    elif alg_name == ALGORITHM_NAME.ASTAR:
        return astar.astar(d, start_pos, end_pos, costMatrix, myMaze, *args)
    elif alg_name == ALGORITHM_NAME.TELE:
        return teleport.teleportSearch(d, start_pos, end_pos, costMatrix, myMaze, *args)
    return None



def get_all_search_algorithms():
    return ['bfs', 'dfs', 'ucs', 'greedy', 'astart']


def get_files(dirPath):
    return [f for f in os.listdir(dirPath) if os.path.isfile(os.path.join(dirPath, f))]


def write_output_txt(filename, matrix, time, cost, route):
    with open(filename, 'w') as f:
        for i in matrix:
            for j in i:
                f.write(j)
            f.write('\n')
        # write time
        f.write(str(time) + '\n')

        f.write(str(cost) + '\n')

        for t in route:
            if t != route[-1]:
                f.write(str(t) + ', ')
            else:
                f.write(str(tuple(t)))
