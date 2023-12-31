import Maze

from general import *
import heuristic

MAX = G_MAX


def greedy(matrix, start, end, costMatrix, maze, *args):
    numRows = len(matrix)
    numCols = len(matrix[0])
    cell_open = 0

    route = [start]
    cell_open += 1

    cost = 0

    isVisited = [[False] * numCols for _ in range(numRows)]
    isVisited[start[0]][start[1]] = True

    while route[-1] != end:
        v = route[-1]
        # Tim o (xx,yy) lan can v, chua duoc tham co heuristic nho nhat
        xx = -1
        yy = -1
        minn = MAX
        for i in range(numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if check(matrix, x, y) is True and isVisited[x][y] is False:
                f = heuristic.h([x, y], end, args)
                if f < minn:
                    minn = f
                    xx = x
                    yy = y
        # Khong co o nao di duoc
        if minn == MAX:
            break
        # Chon o co heuristic nho nhat va di den do
        route.append((xx, yy))
        cell_open += 1

        cost = cost + costMatrix[xx][yy]
        isVisited[xx][yy] = True
        maze.update_cell([yy, xx], Maze.Cell.FRONTIER)
        # print(cost, " -> ", route)
    # print(route)
    if list(route[-1]) == end:
        return cell_open, (cost, route)
    # print(route)
    return cell_open, (MAX, route)
