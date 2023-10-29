import Maze
from general import *
import heapq

MAX = G_MAX


def ucs(matrix, start, end, costMatrix, maze, *args):
    # append -> them vao cuoi
    # queue.remove(queue[0]) -> xoa dau

    numRows = len(matrix)
    numCols = len(matrix[0])

    queue = []
    # queue.append(start)
    heapq.heappush(queue, start)

    cost = [[MAX] * numCols for _ in range(numRows)]
    cost[start[0]][start[1]] = 0

    while queue:
        # queue.sort()
        # v = queue[0]
        # queue.remove(queue[0])
        v = heapq.heappop(queue)

        for i in range(numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if check(matrix, x, y) is True and cost[x][y] == MAX:
                tmpCost = cost[v[0]][v[1]] + costMatrix[x][y]

                cost[x][y] = tmpCost
                heapq.heappush(queue, (x, y))
                maze.update_cell([y, x], Maze.Cell.FRONTIER)

                if [x, y] == end:
                    return trace(matrix, cost, costMatrix, start, end)
    return MAX, []
