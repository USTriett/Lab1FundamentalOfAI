import Maze
from general import *

MAX = G_MAX


def dfs(matrix, start, end, costMatrix, maze, *args):
    # append -> them vao cuoi
    # pop -> xoa cuoi

    numRows = len(matrix)
    numCols = len(matrix[0])

    stack = [start]

    cost = [[MAX] * numCols for _ in range(numRows)]
    cost[start[0]][start[1]] = 0

    while stack:
        v = stack.pop()
        # print("pop ", v)
        maze.update_cell([v[1], v[0]], Maze.Cell.FRONTIER)

        for i in range(numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if (check(matrix, x, y) is True) and (cost[x][y] == MAX):
                stack.append((x, y))
                cost[x][y] = cost[v[0]][v[1]] + costMatrix[x][y]
                if [x, y] == end:
                    return trace(matrix, cost, costMatrix, start, end)
                # print("add ", (x,y))

    return MAX, []
