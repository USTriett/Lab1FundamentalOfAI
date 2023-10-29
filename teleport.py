import Maze
from general import *
from heuristic import *
import heapq

from maze_data import MazeData


def read_file_teleport(filename):
    # mo file
    f = open(filename, 'r')

    # so diem thuong
    n_teleports = int(next(f)[:-1])

    # danh sach diem thuong: x y diem
    teleports = []

    for i in range(n_teleports):
        x1, y1, x2, y2 = map(int, next(f)[:-1].split(' '))
        teleports.append((x1, y1, x2, y2))

    # doc me cung
    text = f.read()
    matrix = [list(i) for i in text.splitlines()]
    f.close()
    goal_pos = find_end(matrix)
    # tra ve: danh sach teleports & me cung
    md = MazeData(0, [], matrix, goal_pos)
    return teleports,md


# find tele dest
def findToTeleports(vx, vy, teleports):
    teleportTo = []

    for x in teleports:
        if vx == x[0] and vy == x[1]:
            teleportTo.append((x[2], x[3]))

    return teleportTo


# find start
def findFromTeleports(vx, vy, teleports):
    teleportFrom = []

    for x in teleports:
        if vx == x[2] and vy == x[3]:
            teleportFrom.append((x[0], x[1]))

    return teleportFrom


def traceTeleports(cntMatrix, teleports, matrix, cost, costMatrix, start, end):
    route = [end]
    v = end
    while v != start:
        teleportFrom = findFromTeleports(v[0], v[1], teleports)
        for x, y in teleportFrom:
            if check(matrix, x, y) is True and cost[x][y] == cost[v[0]][v[1]]:
                route.append((x, y))
                v = (x, y)
                break

        for i in range(numNeibour):
            x = v[0] - adjX[i]
            y = v[1] - adjY[i]
            if check(matrix, x, y) is True and cost[x][y] == cost[v[0]][v[1]] - costMatrix[v[0]][v[1]]:
                route.append((x, y))
                v = (x, y)
                break
    route.reverse()

    return cntMatrix, cost[end[0]][end[1]], route


def teleportSearch(matrix, start, end, costMatrix, maze, *args):
    numRows = len(matrix)
    numCols = len(matrix[0])
    teleports = args[1]
    cntMatrix = [[0] * numCols for _ in range(numRows)]

    queue = []
    heapq.heappush(queue, (0, start[0], start[1]))
    cntMatrix[start[0]][start[1]] += 1

    isClosed = [[False] * numCols for _ in range(numRows)]

    cost = [[G_MAX] * numCols for _ in range(numRows)]
    cost[start[0]][start[1]] = 0

    while queue:
        _, vx, vy = heapq.heappop(queue)
        if matrix[vx][vy] == 'T':
            maze.update_cell([vy, vx], Maze.Cell.CLOSED_GATE)
        if isClosed[vx][vy] is True:
            continue

        isClosed[vx][vy] = True

        for i in range(numNeibour):
            x = vx + adjX[i]
            y = vy + adjY[i]
            tmpCost = cost[vx][vy] + costMatrix[x][y]

            if check(matrix, x, y) is True and isClosed[x][y] is False:
                cost[x][y] = tmpCost
                f = cost[vx][vy] + h([x, y], end, args[0])

                heapq.heappush(queue, (f, x, y))
                maze.update_cell([y, x], Maze.Cell.FRONTIER)
                cntMatrix[x][y] += 1
                # print(f,x,y)
                if (x, y) == end:
                    return traceTeleports(cntMatrix, teleports, matrix, cost, costMatrix, start, end)

        teleportTo = findToTeleports(vx, vy, teleports)
        print(teleportTo)
        for x, y in teleportTo:
            if isClosed[x][y] is False:
                cost[x][y] = cost[vx][vy]
                f = cost[vx][vy] + h([x, y], end, args[0])
                heapq.heappush(queue, (f, x, y))
                maze.update_cell([y, x], Maze.Cell.FRONTIER)

                cntMatrix[x][y] += 1
                # print(f,x,y)
                if (x, y) == end:
                    return traceTeleports(cntMatrix, teleports, matrix, cost, costMatrix, start, end)

    return cntMatrix, G_MAX, []

# def main():
#     teleports, matrix = read_file_teleport(filename="teleport.txt")
#     start = find_start(matrix)
#     end = find_end(matrix)
#     costMatrix = creatCostMatrix(matrix, [])
#
#     cntMatrix, cost, route = teleportSearch(teleports, matrix, start, end, costMatrix)
#     print(cost)
#     print(route)
#     for i in range(len(matrix)):
#         print(cntMatrix[i])
#
#
# main()
