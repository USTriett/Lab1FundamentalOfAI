MAX = 10**8

adjX = [-1,0,1, 0]
adjY = [ 0,1,0,-1]
numNeibour = 4

def read_file(file_name: str = 'maze_map.txt'):
    # mo file
    f=open(file_name,'r')

    # so diem thuong
    n_bonus_points = int(next(f)[:-1])

    # danh sach diem thuong: x y diem
    bonus_points = []
    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    # doc me cung
    text=f.read()
    matrix=[list(i) for i in text.splitlines()]
    f.close()

    # tra ve: danh sach diem thuong & me cung
    return bonus_points, matrix

def find_start(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    for i in range (numRows):
        for j in range (numCols):
            if (matrix[i][j] == 'S'):
                return (i,j)
            
def find_end(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    for i in range (numRows):
        if (matrix[i][0] == ' '):
            return (i,0)
        elif (matrix[i][numCols - 1] == ' '):
            return (i,numCols - 1)
        
    for j in range (numCols):
        if (matrix[0][j] == ' '):
            return (0,j)
        elif (matrix[numRows - 1][j] == ' '):
            return (numRows - 1, j)
    
def creatCostMatrix(matrix, bonus_points):
    switcher = {
        'x': MAX,
        ' ': 1,
        'S': 0,
        '+': -1, 
        # '+' khong quan trong vi se update sau
    }

    numRows = len(matrix)
    numCols = len(matrix[0])
    
    cost = [[switcher.get(matrix[i][j]) for j in range (numCols)] for i in range (numRows)]

    for i in range (len(bonus_points)):
        x = bonus_points[i][0]
        y = bonus_points[i][1]
        reward = bonus_points[i][2]
        cost[x][y] = reward

    return cost

def isInMatrix(matrix,x,y):
    if (x < 0):
        return False
    if (y < 0):
        return False
    if (x >= len(matrix)):
        return False
    if (y >= len(matrix[0])):
        return False
    return True

def check(matrix,x,y):
    if (isInMatrix(matrix, x,y) == True):
        return (matrix[x][y] != 'x')
    return False

def trace(matrix,cost, costMatrix, start, end):
    route = [end]
    v = end
    while (v != start):
        for i in range (numNeibour):
            x = v[0] - adjX[i]
            y = v[1] - adjY[i]
            if (check(matrix,x,y) == True and cost[x][y] == cost[v[0]][v[1]] - costMatrix[v[0]][v[1]]):
                route.append((x,y))
                v = (x,y)
                break
    route.reverse()

    return cost[end[0]][end[1]], route