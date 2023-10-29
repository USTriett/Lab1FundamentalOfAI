from general import *


def calcDistance(matrix, start, costMatrix):
    numRows = len(matrix)
    numCols = len(matrix[0])

    queue = [start]

    cost = [[G_MAX] * numCols for _ in range(numRows)]

    if matrix[start[0]][start[1]] == 'x':
        return cost

    cost[start[0]][start[1]] = 0

    while queue:
        v = queue[0]
        queue.remove(queue[0])

        for i in range(numNeibour):
            x = v[0] + adjX[i]
            y = v[1] + adjY[i]
            if check(matrix, x, y) is True and cost[x][y] == G_MAX:
                cost[x][y] = cost[v[0]][v[1]] + costMatrix[x][y]
                queue.append((x, y))

    return cost


def getBit(mask, _id):
    return (mask >> _id) & 1


def turnOnBit(mask, _id):
    return mask | (1 << _id)


def tracePickpoint(matrix, start, end, distance, cost, traceDp, pickpoints):
    num_pickpoints = len(pickpoints)

    mask_max = 1 << num_pickpoints

    _id = 0
    mask = (mask_max - 1)
    minCost = cost[0]
    for i in range(1, num_pickpoints):
        if cost[i] < minCost:
            _id = i
            minCost = cost[i]

    route = []
    cur = end
    pre = (pickpoints[_id][0], pickpoints[_id][1])
    cont = True

    while cur != start:
        px = pre[0]
        py = pre[1]
        while cur != pre:
            route.append(cur)
            cx = cur[0]
            cy = cur[1]

            ok = False
            for i in range(numNeibour):
                x = cx - adjX[i]
                y = cy - adjY[i]
                if (check(matrix, x, y) is True and distance[px][py][cx][cy] == distance[px][py][x][y] +
                        distance[x][y][cx][cy]):
                    cur = (x, y)
                    ok = True
                    break

            if ok is False:
                return G_MAX, []

        if cont is False:
            break
        if traceDp[mask][_id] == _id:
            pre = start
            cont = False
        else:
            pre = (pickpoints[traceDp[mask][_id]][0], pickpoints[traceDp[mask][_id]][1])
            tmpid = traceDp[mask][_id]
            mask = mask ^ (1 << _id)
            _id = tmpid

    route.append(start)

    return minCost, route


def pickpointSearch(matrix, start, end, costMatrix, maze, *args):
    pickpoints = args[0]
    print(pickpoints)
    num_pickpoints = len(pickpoints)

    numRows = len(matrix)
    numCols = len(matrix[0])

    mask_max = (1 << num_pickpoints)

    distance = [[[]] * numCols for _ in range(numRows)]

    for i in range(numRows):
        for j in range(numCols):
            tmp_dist = calcDistance(matrix, (i, j), costMatrix)
            distance[i][j] = tmp_dist

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

    cost = []
    for i in range(num_pickpoints):
        x1 = pickpoints[i][0]
        y1 = pickpoints[i][1]
        x2 = end[0]
        y2 = end[1]
        cost.append(dp[mask_max - 1][i] + distance[x1][y1][x2][y2])

    return tracePickpoint(matrix, start, end, distance, cost, traceDp, pickpoints)


# def main():
#     pickpoints, matrix = read_file("pickpoint.txt")
#     costMatrix = creatCostMatrix(matrix, pickpoints)
#     start = find_start(matrix)
#     end = find_end(matrix)
#
#     cost, route = pickpointSearch(matrix, start, end, costMatrix, pickpoints)
#
#     print(cost)
#     print(route)
#
#
# main()
