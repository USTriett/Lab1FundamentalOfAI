import os
import matplotlib.pyplot as plt
from general import *
from dfs import *
from bfs import *
from ucs import *
from greedy import *
from astar import *

def main():
    bonus_points, matrix = read_file()

    start = find_start(matrix)
    end = find_end(matrix)

    costMatrix = creatCostMatrix(matrix, bonus_points)

    # print("start = ", start)
    # print("end = ", end)

    # print("costMatrix", costMatrix)
    
    # costDFS, routeDFS = dfs(matrix, start, end, costMatrix)
    # print("DFS")
    # print(costDFS)
    # print(routeDFS)

    # costBFS, routeBFS = bfs(matrix, start, end, costMatrix)
    # print("BFS")
    # print(costBFS)
    # print(routeBFS)
    
    # costUCS, routeUCS = ucs(matrix, start, end, costMatrix)
    # print("UCS")
    # print(costUCS)
    # print(routeUCS)

    # costGreedy, routeGreedy = greedy(matrix, start, end, costMatrix)
    # print("greedy")
    # print(costGreedy)
    # print(routeGreedy)

    costAStar, routeAStar = astar(matrix, start, end, costMatrix)
    print("A*")
    print(costAStar)
    print(routeAStar)

main()