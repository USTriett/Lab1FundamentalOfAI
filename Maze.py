import os
from enum import Enum

import numpy as np
import pygame as pg
import pygame.event
from timeit import default_timer as timer

import astar
import general
import heuristic
import maze_data as md
from pygame_recorder import ScreenRecorder

# print(1)
recorder = ScreenRecorder(1000, 500, 30)


# init pygame
class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "x"
    START = "S"
    GOAL = "G"
    EXPLORED = "E"
    CURRENT = "C"
    FRONTIER = "F"
    PATH = "*"


class Maze:
    __screen = pg.Surface((600, 300))
    __data = None
    __attr = {}

    def __init__(self, size_screen, data, main_screen):

        self.color_map = {Cell.EMPTY: "White", Cell.PATH: "Yellow", Cell.GOAL: "Red", Cell.BLOCKED: "Black",
                          Cell.START: "Green",
                          Cell.FRONTIER: "Purple"}
        self.__main_screen = main_screen
        self.__screen = pg.Surface(size_screen)
        self.__screen.fill("White")
        self.__data = data.copy()
        shape = data.shape
        print(shape)
        self.__width_rec = self.__screen.get_width() // shape[1]
        height_rec = self.__screen.get_height() // shape[0]
        self.__width_rec = min(self.__width_rec, height_rec)

        print(self.__width_rec)

        pos = [0, 0]
        for r in data:
            for c in r:
                # print(c)
                self.__color_pos__(pos[0], pos[1], c)
                # print("" + str(pos) + " " + str(c))
                pos[0] += 1
            pos[1] += 1
            pos[0] = 0

        # pos[0] = 0
        # pos[1] = 0
        # for i in range(0, shape[0] + 1):
        #     pg.draw.line(self.__screen, "Black", pos, ((shape[1]) * self.__width_rec, pos[1]))
        #     # print(((shape[1]) * self.__width_rec, pos[1]))
        #     pos[1] += self.__width_rec
        #
        # pos[1] = 0
        # for i in range(0, shape[1] + 1):
        #     pg.draw.line(self.__screen, "Black", pos, (pos[0], (shape[0]) * self.__width_rec))
        #     pos[0] += self.__width_rec

    def __color_pos__(self, row, col, rect_type):

        pg.draw.rect(self.__screen, self.color_map[rect_type],
                     (row * self.__width_rec, col * self.__width_rec, self.__width_rec, self.__width_rec))

    def update_cell(self, pos, _type):
        # print(self.__data[pos[0]][pos[1]])
        self.__color_pos__(pos[0], pos[1], _type)
        self.display()
        # pygame.time.wait(50)

    def trace_back(self, pos):
        for [i, j] in pos:
            self.update_cell([j, i], Cell.PATH)
            self.display()
            # pygame.time.wait(50)

    def display(self):
        self.__main_screen.blit(self.__screen, (0, 0))
        pygame.display.flip()
        recorder.capture_frame(self.__main_screen)

    def generate_maze(self, file_name):
        pass


# def demoAlg(_maze):
#     d = np.array(_maze.get_data())
#     screen = pg.display.set_mode((1000, 500))
#     screen.fill("White")
#     myMaze = Maze((900, 450), d, screen)
#     myMaze.display()
#     pygame.display.flip()
#     costMatrix = general.creatCostMatrix(d, [])
#     start_pos = general.find_start(d)
#     end_pos = _maze.get_goal_pos()
#     return d, start_pos, end_pos, costMatrix, myMaze

def record_change_output(dest, alg_name, num_of_input, heu=''):
    heuAlg = ''
    if heu != '':
        heuAlg = '_heuristic_' + heu
    fileout = '/' + alg_name + heuAlg
    os.makedirs(dest + str(num_of_input) + '/' + alg_name, exist_ok=True)
    recorder.change_output_file(dest + str(num_of_input) + '/' + alg_name + fileout + '.mp4')
    return dest + str(num_of_input) + '/' + alg_name + fileout


def main(level, alg_name, h=''):
    dirPath = "./input/level_" + str(level)
    myMazeData = []
    filenames = general.get_files(dirPath)
    for f in filenames:
        myMazeData.append(md.read_data(os.path.join(dirPath, f)))
    pg.init()
    count = 1
    outDirPath = './output/level' + str(level) + '/input'
    for maze in myMazeData:
        path = record_change_output(outDirPath, alg_name, count, h)

        d = np.array(maze.get_data())
        screen = pg.display.set_mode((1000, 500))
        screen.fill("White")
        myMaze = Maze((900, 450), d, screen)
        myMaze.display()
        pygame.display.flip()
        costMatrix = general.creatCostMatrix(d, [])
        start_pos = general.find_start(d)
        end_pos = maze.get_goal_pos()
        preSum = 0
        if h == '2':
            preSum = heuristic.calcPrefixSum(d)
            # print(preSum)
        # print(preSum)
        start_time = timer()
        cost, route = general.get_func_dict(alg_name, d, start_pos, end_pos, costMatrix, myMaze, preSum)
        # print(route)
        end_time = timer()
        general.write_output_txt(path + '.txt', [], end_time - start_time, cost, route)
        count += 1
        # print(count, end_time - start_time)
        myMaze.trace_back(route)
        for i in range(50):
            recorder.capture_frame(screen)
        pg.quit()
        recorder.end_recording()
