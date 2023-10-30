from general import *


# chay level 2 thoi
def calcDistance(matrix, start, costMatrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    queue = [start]

    cost = [[G_MAX] * numCols for _ in range(numRows)]
    traceBFS = [[[-1, -1]] * numCols for _ in range(numRows)]

    if matrix[start[0]][start[1]] == 'x':
        return cost, traceBFS

    traceBFS[start[0]][start[1]] = list(start)
    cost[start[0]][start[1]] = 0

    while queue:
        v = queue[0]
        queue.remove(queue[0])

        for i in range(numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if check(matrix, x, y) == True and cost[x][y] == G_MAX:
                cost[x][y] = cost[v[0]][v[1]] + costMatrix[x][y]
                queue.append((x, y))
                traceBFS[x][y] = list(v)

    # print(start)
    # for i in range (numRows):
    #     for j in range (numCols):
    #         if cost[i][j] == G_MAX:
    #             print(-1, end=" ")
    #         else:
    #             print(cost[i][j], end = " ")
    #     print()
    return cost, traceBFS


def getBit(mask, _id):
    return (mask >> _id) & 1


def turnOnBit(mask, _id):
    return (mask | (1 << _id))


def tracebonuspoint(start, end, cost, traceDp, bonuspoints, traceBFS):
    num_bonuspoints = len(bonuspoints)

    mask_max = 1 << num_bonuspoints

    _id = -1
    mask = -1
    minCost = G_MAX
    for cur_mask in range(mask_max):
        for last in range(num_bonuspoints):
            if cost[cur_mask][last] < minCost:
                _id = last
                mask = cur_mask
                minCost = cost[cur_mask][last]

    route = []
    cur = list(end)
    if _id == -1:
        pre = list(start)
    else:
        pre = [bonuspoints[_id][0], bonuspoints[_id][1]]

    # trace
    while cur[0] != start[0] or cur[1] != start[1]:
        # print(_id, cur, pre)
        # print(mask, _id)
        px = pre[0]
        py = pre[1]

        # find path between start -> bonus -> bonus -> end
        while cur[0] != pre[0] or cur[1] != pre[1]:
            route.append(cur)
            cx = cur[0]
            cy = cur[1]

            tmp = traceBFS[px][py][cx][cy]
            if tmp[0] == -1 and tmp[1] == -1:
                return G_MAX, []
            cur = tmp

        if pre == list(start):
            break
        if traceDp[mask][_id] == _id:
            pre = list(start)
        else:
            # print("traceDP: ", traceDp[mask][_id])
            pre = [bonuspoints[traceDp[mask][_id]][0], bonuspoints[traceDp[mask][_id]][1]]
            tmp_id = traceDp[mask][_id]
            mask = mask ^ (1 << _id)
            # print("trace: ", mask, _id, " = ", tmp_id)            
            _id = tmp_id

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


def bonuspointSearch(matrix, start, end, costMatrix, maze, score_data):
    bonuspoints = score_data[0]
    num_bonuspoints = len(bonuspoints)

    numRows = len(matrix)
    numCols = len(matrix[0])

    mask_max = (1 << num_bonuspoints)

    distance = [[[]] * numCols for _ in range(numRows)]
    traceBFS = [[[]] * numCols for _ in range(numRows)]

    for i in range(numRows):
        for j in range(numCols):
            tmp_dist, tmp_trace = calcDistance(matrix, (i, j), costMatrix)

            distance[i][j] = tmp_dist
            traceBFS[i][j] = tmp_trace

    dp = [[G_MAX] * num_bonuspoints for _ in range(mask_max)]
    traceDp = [[-1] * num_bonuspoints for _ in range(mask_max)]

    for i in range(num_bonuspoints):
        mask = (1 << i)
        x1 = start[0]
        y1 = start[1]
        x2 = bonuspoints[i][0]
        y2 = bonuspoints[i][1]
        dp[mask][i] = distance[x1][y1][x2][y2]
        traceDp[mask][i] = i

    for mask in range(mask_max):
        for last in range(num_bonuspoints):
            if getBit(mask, last) == 1:
                for newlast in range(num_bonuspoints):
                    if getBit(mask, newlast) == 0:
                        newmask = turnOnBit(mask, newlast)
                        x1 = bonuspoints[last][0]
                        y1 = bonuspoints[last][1]
                        x2 = bonuspoints[newlast][0]
                        y2 = bonuspoints[newlast][1]
                        c = dp[mask][last] + distance[x1][y1][x2][y2]
                        if c < dp[newmask][newlast]:
                            dp[newmask][newlast] = c
                            traceDp[newmask][newlast] = last
                            # print(toBin(mask), " -> ", toBin(newmask), " - ", c, " - ", newlast)

    cost = [[0] * num_bonuspoints for _ in range(mask_max)]

    for last in range(num_bonuspoints):
        x2 = end[0]
        y2 = end[1]
        x1 = bonuspoints[last][0]
        y1 = bonuspoints[last][1]
        for mask in range(mask_max):
            cost[mask][last] = dp[mask][last] + distance[x1][y1][x2][y2]

    return tracebonuspoint(start, end, cost, traceDp, bonuspoints, traceBFS)
