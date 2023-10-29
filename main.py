import os

import Maze
import general
import heuristic
import maze_data as md
import pygame as pg
if __name__ == '__main__':
    pg.init()
    level = 1
    algs = [general.ALGORITHM_NAME.BFS, general.ALGORITHM_NAME.DFS, general.ALGORITHM_NAME.UCS,
            general.ALGORITHM_NAME.GREEDY, general.ALGORITHM_NAME.ASTAR]
    heu = ['1', '2']
    # for i in range(1, level + 1):
    #     for alg in algs:
    #         if alg != algs[-1] and alg != algs[-2]:
    #             Maze.main(1, alg)
    #             # print("pass")
    #         else:
    #             for h in heu:
    #                 print(alg, h)
    #                 Maze.main(1, alg, h)

    Maze.advanced_main(general.ALGORITHM_NAME.TELE, h='1')
