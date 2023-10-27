from general import *
from heuristic import *

def greedy(matrix, start, end, costMatrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    route = [start]
    cost = 0

    isVisited = [[False]* numCols for _ in range (numRows)]
    isVisited[start[0]][start[1]] = True

    while (route[-1] != end):
        v = route[-1]
        # Tim o (xx,yy) lan can v, chua duoc tham co heuristic nho nhat
        xx = -1
        yy = -1
        minn = MAX
        for i in range (numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if (check(matrix,x,y) == True and isVisited[x][y] == False):
                h = h1((x,y), end)
                if (h < minn):
                    minn = h
                    xx = x
                    yy = y
        # Khong co o nao di duoc
        if (minn == MAX):
            return MAX,[]
        # Chon o co heuristic nho nhat va di den do
        route.append((xx,yy))
        cost = cost + costMatrix[xx][yy]
        isVisited[xx][yy] = True
        # print(cost, " -> ", route)

    return cost, route

        
                    
