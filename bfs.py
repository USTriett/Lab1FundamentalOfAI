import pygame.time

import Maze
from general import *

MAX = G_MAX


def bfs(matrix, start, end, costMatrix, maze, *args):
    # append -> them vao cuoi
    # popleft -> xoa dau

    numRows = len(matrix)
    numCols = len(matrix[0])

    queue = [start]

    cost = [[MAX] * numCols for _ in range(numRows)]
    cost[start[0]][start[1]] = 0

    while queue:
        v = queue[0]
        queue.remove(queue[0])

        for i in range(numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if check(matrix, x, y) is True and cost[x][y] == MAX:

                cost[x][y] = cost[v[0]][v[1]] + costMatrix[x][y]
                queue.append((x, y))

                maze.update_cell([y, x], Maze.Cell.FRONTIER)

                if [x, y] == end:
                    return trace(matrix, cost, costMatrix, start, end)
    return MAX, []
