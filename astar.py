from general import *

def heristicASTAR():
    return 0

def astar(matrix, start, end, costMatrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    queue = []
    queue.append([0,start[0],start[1]])

    isClosed = [[False] * numCols for _ in range (numRows)]

    cost = [[MAX] * numCols for _ in range (numRows)]
    cost[start[0]][start[1]] = 0

    while (queue):
        queue.sort()
        c,vx,vy = queue[0]
        queue.remove(queue[0])
        isClosed[vx][vy] = True

        if ((vx,vy)==end):
            return trace(matrix,cost, costMatrix, start, end)
        
        for i in range (numNeibour):
            x = vx + adjX[i]
            y = vy + adjY[i]
            tmpCost = cost[vx][vy] + costMatrix[x][y]
            if (check(matrix, x,y) == True and isClosed[x][y]==False):
                cost[x][y] = tmpCost
                h = cost[vx][vy] + heristicASTAR()
                queue.append((h,x,y))
    return MAX,[]