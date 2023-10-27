from general import *

def bfs(matrix, start, end, costMatrix):
    # append -> them vao cuoi
    # popleft -> xoa dau

    numRows = len(matrix)
    numCols = len(matrix[0])

    queue = []
    queue.append(start)

    cost = [[MAX] * numCols for _ in range (numRows)]
    cost[start[0]][start[1]] = 0

    while (queue):
        v = queue[0]
        queue.remove(queue[0])

        if (v==end):
            return trace(matrix,cost, costMatrix, start, end)
        
        for i in range (numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if (check(matrix, x,y) == True and cost[x][y] == MAX):
                cost[x][y] = cost[v[0]][v[1]] + costMatrix[x][y]
                queue.append((x,y))
    return MAX,[]