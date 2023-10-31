import Maze
from general import *
import heapq

MAX = G_MAX


def ucs(matrix, start, end, costMatrix, maze, *args):
    # append -> them vao cuoi
    # queue.remove(queue[0]) -> xoa dau

    numRows = len(matrix)
    numCols = len(matrix[0])
    cell_open = 0

    queue = []
    # queue.append(start)
    heapq.heappush(queue, [0,start[0],start[1]])
    cell_open += 1
    cost = [[MAX] * numCols for _ in range(numRows)]
    cost[start[0]][start[1]] = 0

    while queue:
        # queue.sort()
        # v = queue[0]
        # queue.remove(queue[0])
        c,vx,vy= heapq.heappop(queue)

        for i in range(numNeibour):
            x = vx + adjX[i]
            y = vy + adjY[i]
            if check(matrix, x, y) is True and cost[x][y] == MAX:
                tmpCost = cost[vx][vy] + costMatrix[x][y]

                cost[x][y] = tmpCost
                heapq.heappush(queue, (cost[x][y] ,x, y))
                cell_open += 1

                maze.update_cell([y, x], Maze.Cell.FRONTIER)

                if [x, y] == end:
                    return cell_open, trace(matrix, cost, costMatrix, start, end)
    return cell_open, (MAX, [])
