from general import *

def dfs(matrix, start, end, costMatrix):
    # append -> them vao cuoi
    # pop -> xoa cuoi

    numRows = len(matrix)
    numCols = len(matrix[0])

    stack = []
    stack.append(start)

    cost = [[MAX] * numCols for _ in range(numRows)]
    cost[start[0]][start[1]] = 0

    while (stack):
        v = stack.pop()
        # print("pop ", v)
        
        if (v == end):
            return trace(matrix, cost, costMatrix, start, end)

        for i in range (numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if ((check(matrix,x,y) == True) and (cost[x][y] == MAX)):
                stack.append((x, y))
                cost[x][y] = cost[v[0]][v[1]] + costMatrix[x][y]
                # print("add ", (x,y))

    return MAX, []