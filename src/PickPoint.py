from general import *

#chay level 3 thoi
def calcDistance(matrix, start, costMatrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    queue = []
    queue.append(start)

    cost = [[G_MAX] * numCols for _ in range(numRows)]
    traceBFS = [[[-1, -1]] * numCols for _ in range(numRows)]

    if matrix[start[0]][start[1]] == 'x':
        return cost, traceBFS

    traceBFS[start[0]][start[1]] = list(start)
    cost[start[0]][start[1]] = 0

    while (queue):
        v = queue[0]
        queue.remove(queue[0])

        for i in range(numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if (check(matrix, x, y) == True and cost[x][y] == G_MAX):
                cost[x][y] = cost[v[0]][v[1]] + costMatrix[x][y]
                queue.append((x, y))
                traceBFS[x][y] = list(v)

    return cost, traceBFS


def getBit(mask, id):
    return (mask >> id) & 1


def turnOnBit(mask, id):
    return (mask | (1 << id))


def tracePickpoint(start, end, cost, traceDp, pickpoints, traceBFS):
    num_pickpoints = len(pickpoints)

    mask_max = 1 << num_pickpoints

    id = 0
    mask = (mask_max - 1)
    minCost = cost[0]
    for i in range(1, num_pickpoints):
        if cost[i] < minCost:
            id = i
            minCost = cost[i]

    route = []
    cur = list(end)
    pre = [pickpoints[id][0], pickpoints[id][1]]
    cont = True

    while cur[0] != start[0] or cur[1] != start[1]:
        # print(cur, pre)
        px = pre[0]
        py = pre[1]
        while cur[0] != pre[0] or cur[1] != pre[1]:
            route.append(cur)
            cx = cur[0]
            cy = cur[1]

            tmp = traceBFS[px][py][cx][cy]
            if tmp[0] == -1 and tmp[1] == -1:
                return MAX, []
            cur = tmp

        if cont is False:
            break
        if traceDp[mask][id] == id:
            pre = list(start)
            cont = False
        else:
            pre = [pickpoints[traceDp[mask][id]][0], pickpoints[traceDp[mask][id]][1]]
            tmpid = traceDp[mask][id]
            mask = mask ^ (1 << id)
            id = tmpid

    route.append(list(start))
    route.reverse()
    return minCost, route


def toBin(x):
    s = ""
    while x > 0:
        if x % 2 == 0:
            s = '0' + s
        else:
            s = '1' + s
        x //= 2
    return s


def pickpointSearch(matrix, start, end, costMatrix, maze, *args):

    pickpoints = args[0][0]
    # print(pickpoints)
    num_pickpoints = len(pickpoints)

    numRows = len(matrix)
    numCols = len(matrix[0])

    mask_max = (1 << num_pickpoints)

    distance = [[[]] * numCols for _ in range(numRows)]
    traceBFS = [[[]] * numCols for _ in range(numRows)]

    for i in range(numRows):
        for j in range(numCols):
            tmp_dist, tmp_trace = calcDistance(matrix, (i, j), costMatrix)

            distance[i][j] = tmp_dist
            traceBFS[i][j] = tmp_trace

    dp = [[G_MAX] * num_pickpoints for _ in range(mask_max)]
    traceDp = [[-1] * num_pickpoints for _ in range(mask_max)]

    for i in range(num_pickpoints):
        mask = (1 << i)
        x1 = start[0]
        y1 = start[1]
        x2 = pickpoints[i][0]
        y2 = pickpoints[i][1]
        dp[mask][i] = distance[x1][y1][x2][y2]
        traceDp[mask][i] = i

    for mask in range(mask_max):
        for last in range(num_pickpoints):
            if getBit(mask, last) == 1:
                for newlast in range(num_pickpoints):
                    if getBit(mask, newlast) == 0:
                        newmask = turnOnBit(mask, newlast)
                        x1 = pickpoints[last][0]
                        y1 = pickpoints[last][1]
                        x2 = pickpoints[newlast][0]
                        y2 = pickpoints[newlast][1]
                        c = dp[mask][last] + distance[x1][y1][x2][y2]
                        if c < dp[newmask][newlast]:
                            dp[newmask][newlast] = c
                            traceDp[newmask][newlast] = last
                            # print(toBin(mask), " -> ", toBin(newmask), " - ", c, " - ", newlast)

    cost = []
    for i in range(num_pickpoints):
        x1 = pickpoints[i][0]
        y1 = pickpoints[i][1]
        x2 = end[0]
        y2 = end[1]
        cost.append(dp[mask_max - 1][i] + distance[x1][y1][x2][y2])

    return tracePickpoint(start, end, cost, traceDp, pickpoints, traceBFS)



