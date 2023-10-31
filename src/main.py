import os

import Maze
import general

if __name__ == '__main__':
    level = 3
    algs = [general.ALGORITHM_NAME.BFS, general.ALGORITHM_NAME.DFS, general.ALGORITHM_NAME.UCS,
            general.ALGORITHM_NAME.GREEDY, general.ALGORITHM_NAME.ASTAR]
    heu = ['1', '2', '4']
    # Maze.main(1, general.ALGORITHM_NAME.GREEDY, '1')
    # level 1
    print("Program starting")

    for alg in algs:
        if alg != algs[-1] and alg != algs[-2]:
            print(alg, 'running')
            Maze.main(1, alg)

        else:
            for h in heu:
                print(alg + '_' + h, 'running')
                # print(alg, h)
                Maze.main(1, alg, h)

    print(general.ALGORITHM_NAME.BONUS, 'running')

    Maze.main(2, general.ALGORITHM_NAME.BONUS)
    print(general.ALGORITHM_NAME.PICKUP, 'running')

    Maze.main(3, general.ALGORITHM_NAME.PICKUP)
    for h in heu:
        print(general.ALGORITHM_NAME.TELE, '_' + h + ' running')
        Maze.advanced_main(alg_name=general.ALGORITHM_NAME.TELE, h=h)
    print("Done! Please check output directory")