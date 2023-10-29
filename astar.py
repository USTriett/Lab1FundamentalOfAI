import Maze
import heuristic
from general import *
from heuristic import *
import heapq

MAX = G_MAX


def astar(matrix, start, end, costMatrix, maze, *args):
    numRows = len(matrix)
    numCols = len(matrix[0])

    queue = []
    # queue.append([0,start[0],start[1]])
    heapq.heappush(queue, [0, start[0], start[1]])

    isClosed = [[False] * numCols for _ in range(numRows)]

    cost = [[MAX] * numCols for _ in range(numRows)]
    cost[start[0]][start[1]] = 0

    while queue:
        # print("priQueue: ", queue)
        # queue.sort()
        # c,vx,vy = queue[0]
        # queue.remove(queue[0])
        c, vx, vy = heapq.heappop(queue)
        if isClosed[vx][vy] is True:
            continue

        isClosed[vx][vy] = True

        for i in range(numNeibour):
            x = vx + adjX[i]
            y = vy + adjY[i]
            tmpCost = cost[vx][vy] + costMatrix[x][y]

            if check(matrix, x, y) is True and isClosed[x][y] is False:
                cost[x][y] = tmpCost
                # print(args)
                f = cost[vx][vy] + h([x, y], end, args)

                # queue.append((h,x,y))
                heapq.heappush(queue, (f, x, y))
                maze.update_cell([y, x], Maze.Cell.FRONTIER)
                # print(queue)
                # print(h, x, y)
                if [x, y] == end:
                    return trace(matrix, cost, costMatrix, start, end)

    return MAX, []
