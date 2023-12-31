import Maze
from general import *
import heuristic
import heapq

MAX = G_MAX


def astar(matrix, start, end, costMatrix, maze, *args):
    numRows = len(matrix)
    numCols = len(matrix[0])
    cell_open = 0
    queue = []
    # queue.append([0,start[0],start[1]])
    heapq.heappush(queue, [0, start[0], start[1]])
    cell_open += 1
    isClosed = [[False] * numCols for _ in range(numRows)]

    cost = [[MAX] * numCols for _ in range(numRows)]
    cost[start[0]][start[1]] = 0
    while queue:
        # print("priQueue: ", queue)
        # queue.sort()
        # c,vx,vy = queue[0]
        # queue.remove(queue[0])
        c, vx, vy = heapq.heappop(queue)
        # print(vx, vy)
        if isClosed[vx][vy] is True:
            continue

        isClosed[vx][vy] = True

        for i in range(numNeibour):
            x = vx + adjX[i]
            y = vy + adjY[i]
            # print(x, y)
            if check(matrix, x, y) is True and isClosed[x][y] is False:
                tmpCost = cost[vx][vy] + costMatrix[x][y]

                cost[x][y] = tmpCost
                # print(args)
                f = cost[vx][vy] + heuristic.h([x, y], end, args)

                # queue.append((h,x,y))
                heapq.heappush(queue, (f, x, y))
                cell_open += 1
                maze.update_cell([y, x], Maze.Cell.FRONTIER)

                if [x, y] == end:
                    # print('end')
                    return cell_open, trace(matrix, cost, costMatrix, start, end)

    return cell_open, (MAX, [])
