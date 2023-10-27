# Heuristic 1: dung khoang cach Mahatan giua diem dang xet va dich
def h1(cur, end):
    # Mahatan
    return abs(cur[0]-end[0]) + abs(cur[1]-end[1])

# Heuristic 2: Heuristic 1 + tinh so vat can trong HCN nho nhat chua diem dang xet va dich
def calcPrefixSum(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    prefixSum = [[0] * (numCols + 1) for _ in range (numRows + 1)]

    for i in range (1,numRows + 1):
        for j in range (1,numCols + 1):
            prefixSum[i][j] = prefixSum[i-1][j] + prefixSum[i][j-1] - prefixSum[i-1][j-1] + (matrix[i-1][j-1] == 'x')

    return prefixSum

def calcInRect(prefixSum, left, right, top, bottom):
    left = left + 1
    right = right + 1
    top = top + 1
    bottom = bottom + 1

    return prefixSum[right][bottom] - prefixSum[right][top-1] - prefixSum[left-1][bottom] + prefixSum[left-1][top-1]

def h2(cur, end, prefixSum):
    # xac dinh cac canh cua HCN
    top = min(cur[0],end[0])
    left = min(cur[1],end[1]) 
    right = max(cur[0],end[0])
    bottom = max(cur[1],end[1])

    # so vat can
    c = calcInRect(prefixSum, left, right, top, bottom)

    # Mahatan + so vat can trong HCN (cur, end)
    return h1(cur,end) + c

# Heuristic 3: Heuristic 1 + tinh so vat can trong tam giac vuong can \
# tu diem hien tai (la 1 dinh khong vuong) sang trai/phai
def calcPreSumCols(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    prefixSum = [[0] * (numCols + 1) for _ in range (numRows + 1)]
    # prefixSum[x]: tong cong don cua cot x

    for i in range (1,numRows + 1):
        for j in range (1,numCols + 1):
            prefixSum[j][i] = prefixSum[j][i-1] + (matrix[i-1][j-1] == 'x')

    return prefixSum

def calcInCol(bottom, len, preSumCol):
    bottom = bottom + 1

    return preSumCol[bottom] - preSumCol[bottom-len]

def h3(cur, end, len, direction,  preSumCols):
    # tinh so vat can trong tam giac vuong can
    # cur: diem dang xet (1 dinh khong vuong)
    # len: do dai canh goc vuong
    # direction: -1 -> sang trai; 1 -> sang phai
    # preSumCols: tong tien to theo cot

    cnt = 0
    (x,y) = cur

    for i in range (len):
        cnt = cnt + calcInCol(y,i+1,preSumCols[x])
        x = x + direction # xet cot tiep theo

    return h1(cur,end) + cnt
