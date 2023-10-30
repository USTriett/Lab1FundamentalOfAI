# Heuristic 1: dung khoang cach Mahatan giua diem dang xet va dich
from general import isInMatrix


def h1(arg):
    # print('h1 call')
    cur = arg[0]
    end = arg[1]
    # print(end)
    # matrix = arg[2]
    # print(matrix)
    # Mahatan
    dx = abs(end[0] - cur[0])
    dy = abs(end[1] - cur[1])
    return dx + dy


# Heuristic 2: Heuristic 1 + tinh so vat can trong HCN nho nhat chua diem dang xet va dich
def calcPrefixSum(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    prefixSum = [[0] * (numCols + 1) for _ in range(numRows + 1)]

    for i in range(1, numRows + 1):
        for j in range(1, numCols + 1):
            prefixSum[i][j] = prefixSum[i - 1][j] + prefixSum[i][j - 1] - prefixSum[i - 1][j - 1] + (
                    matrix[i - 1][j - 1] == 'x')

    return prefixSum


def calcInRect(prefixSum, left, right, top, bottom):
    left = left + 1
    right = right + 1
    top = top + 1
    bottom = bottom + 1
    # print(top, bottom, left,  right)
    return prefixSum[bottom][right] - prefixSum[top - 1][right] - prefixSum[bottom][left - 1] + prefixSum[top - 1][
        left - 1]
    # return prefixSum[right][bottom] - prefixSum[right][top - 1] - prefixSum[left - 1][bottom] + prefixSum[left - 1][top - 1]


def h2(args):
    # print('h2 call')
    cur = args[0]
    end = args[1]
    prefixSum = args[2][1]
    # print(prefixSum)
    matrix = args[2][0]

    # xac dinh cac canh cua HCN
    top = min(cur[0], end[0])
    left = min(cur[1], end[1])
    bottom = max(cur[0], end[0])
    right = max(cur[1], end[1])

    # so vat can
    c = calcInRect(prefixSum, left, right, top, bottom)
    a = (abs(left - right) + 1) * (abs(bottom - top) + 1)
    # print(left, right, top, bottom, c)
    # Mahatan + so vat can trong HCN (cur, end)
    h_1 = h1((cur, end, matrix))
    return h_1 + c/a * h_1


# Heuristic 3: Heuristic 1 + tinh so vat can trong tam giac vuong can \
# tu diem hien tai (la 1 dinh khong vuong) sang trai/phai
def calcPreSumCols(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    prefixSum = [[0] * (numCols + 1) for _ in range(numRows + 1)]
    # prefixSum[x]: tong cong don cua cot x

    for i in range(1, numRows + 1):
        for j in range(1, numCols + 1):
            prefixSum[j][i] = prefixSum[j][i - 1] + (matrix[i - 1][j - 1] == 'x')

    return prefixSum


def calcInCol(bottom, len, preSumCol):
    bottom = bottom + 1

    return preSumCol[bottom] - preSumCol[bottom - len]


def h3(args):
    # tinh so vat can trong tam giac vuong can
    # cur: diem dang xet (1 dinh khong vuong)
    # len: do dai canh goc vuong
    # direction: -1 -> sang trai; 1 -> sang phai
    # preSumCols: tong tien to theo cot
    cur = args[0]
    end = args[1]
    len = args[2]
    direction = args[3]
    preSumCols = args[4]
    cnt = 0
    (x, y) = cur

    for i in range(len):
        cnt = cnt + calcInCol(y, i + 1, preSumCols[x])
        x = x + direction  # xet cot tiep theo

    return h1((cur, end)) + cnt


# Heuristic 4:
# manhattan scale ve 1
# scale tong 8 o xung quanh ve 1
def scaleManhattan(cur, end, numRows, numCols):
    dx = abs(end[0] - cur[0])
    dy = abs(end[1] - cur[1])

    return 0.5 * dx / (numRows - 1) + 0.5 * dy / (numCols - 1)


def scaleSurround(cur, matrix):
    surX = [1, 1, 1, -1, -1, -1, 0, 0]
    surY = [1, 0, -1, -1, 0, 1, 1, -1]
    _sum = 0
    numSur = len(surX)
    for i in range(numSur):
        x = cur[0] + surX[i]
        y = cur[1] + surY[i]
        if isInMatrix(matrix, x, y) is True:
            if matrix[x][y] == 'x':
                if abs(surX[i]) + abs(surY[i]) == 1:
                    _sum += 3
                else:
                    _sum += 1

    return float(_sum / 16)


def h4(args):
    cur = args[0]
    end = args[1]
    matrix = args[2]

    # print(cur)

    scaleSur = scaleSurround(cur, matrix)

    # print(scaleM, scaleSur, scaleM + scaleSur)
    h_1 = h1((cur, end))
    return h_1 + scaleSur*h_1


def h(start, end, *args):
    if len(args) == 0:
        return h1((start, end))
    elif len(args) == 1:
        # print(len(args[0]))
        if len(args[0]) == 3:
            return h4((start, end, args[0][0]))
        if len(args[0]) == 0:
            return h1((start, end, []))
        if len(args[0][0]) == 1:
            return h1((start, end, args[0][0]))
        # print(args[0][0])
        # print('h2 called')
        return h2((start, end, args[0][0]))

    elif len(args) == 3:
        return h3((start, end, args[0], args[1]))
    return 0
