import Maze
from src import general

if __name__ == '__main__':
    level = 3
    algs = [general.ALGORITHM_NAME.BFS, general.ALGORITHM_NAME.DFS, general.ALGORITHM_NAME.UCS,
            general.ALGORITHM_NAME.GREEDY, general.ALGORITHM_NAME.ASTAR]
    heu = ['1', '2', '4']
    # Maze.main(1, general.ALGORITHM_NAME.GREEDY, '1')
    # level 1

    for alg in algs:
        if alg != algs[-1] and alg != algs[-2]:
            Maze.main(1, alg)
            # print("pass")
        else:
            for h in heu:
                # print(alg, h)
                Maze.main(1, alg, h)

    for i in range(2, 4):
        Maze.main(i, general.ALGORITHM_NAME.BONUS)
    for h in heu:
        Maze.advanced_main(alg_name=general.ALGORITHM_NAME.TELE, h=h)