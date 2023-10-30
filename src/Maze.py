import os
from enum import Enum
from timeit import default_timer as timer

import numpy as np
import pygame as pg

import pygame.event

from src import heuristic, general, teleport
import maze_data as md
from pygame_recorder import ScreenRecorder

# print(1)
recorder = ScreenRecorder(1000, 500, 30)


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "x"
    START = "S"
    GOAL = "G"
    EXPLORED = "E"
    CURRENT = "C"
    FRONTIER = "F"
    PATH = "*"
    TELE = "T"
    CLOSED_GATE = 'CG'
    SCORE = '+'
    NOPATH = 'no'

class Maze:
    __screen = pg.Surface((600, 300))
    __data = None
    __attr = {}

    # pg.font.init()

    def __init__(self, size_screen, data, main_screen):

        self.color_map = {Cell.EMPTY: "White", Cell.PATH: "Yellow", Cell.GOAL: "Blue", Cell.BLOCKED: "Black",
                          Cell.START: "Green",
                          Cell.FRONTIER: "Purple",
                          Cell.TELE: "Orange",
                          Cell.CLOSED_GATE: "Gray",
                          Cell.SCORE: "White",
                          Cell.NOPATH:"RED"
                          }
        self.__main_screen = main_screen
        self.__screen = pg.Surface(size_screen)
        self.__screen.fill("White")
        self.__data = data.copy()
        # print('end pos', general.find_end(data))
        # print(data)
        shape = data.shape
        # print(shape)
        self.__width_rec = self.__screen.get_width() // shape[1]
        height_rec = self.__screen.get_height() // shape[0]
        self.__width_rec = min(self.__width_rec, height_rec)
        self.__font = general.get_font()

        pos = [0, 0]
        for r in data:
            for c in r:
                # print(c)
                self.__color_pos__(pos[0], pos[1], c)
                # print("" + str(pos) + " " + str(c))
                pos[0] += 1
            pos[1] += 1
            pos[0] = 0

    def __color_pos__(self, row, col, rect_type):

        pg.draw.rect(self.__screen, self.color_map[rect_type],
                     (row * self.__width_rec, col * self.__width_rec, self.__width_rec, self.__width_rec))
        if self.__data[col][row] == Cell.SCORE:
            self.__write_text__(row, col, '+', (self.__width_rec + 5) // 2)
        elif self.__data[col][row] == Cell.GOAL or (col, row) == general.find_end(self.__data):
            self.__write_text__(row, col, 'EXIT', self.__width_rec // 2)
        elif self.__data[col][row] == Cell.START:
            self.__write_text__(row, col, 'S', self.__width_rec // 2)

    def __write_text__(self, x, y, txt, size=0):
        # print(txt)
        if size == 0:
            size = self.__width_rec // 2
        text = general.get_font(size).render(txt, True, "Black")
        self.__screen.blit(text,
                           (x * self.__width_rec + size // 7, y*self.__width_rec + size // 2))

    def update_cell(self, pos, _type):
        # print(self.__data[pos[0]][pos[1]])
        self.__color_pos__(pos[0], pos[1], _type)

        self.display()
        # pygame.time.wait(50)

    def trace_back(self, pos, type_trace):
        for [i, j] in pos:
            self.update_cell([j, i], type_trace)
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

    dirPath = "input/level_" + str(level)
    myMazeData = []
    filenames = general.get_files(dirPath)
    for f in filenames:
        myMazeData.append(md.read_data(os.path.join(dirPath, f)))
        # print(f)
    count = 1
    outDirPath = 'output/level' + str(level) + '/input'
    for maze in myMazeData:
        path = record_change_output(outDirPath, alg_name, count, h)
        d = np.array(maze.get_data())
        screen = pg.display.set_mode((1000, 500))
        screen.fill("White")
        myMaze = Maze((900, 450), d, screen)
        myMaze.display()
        pygame.display.flip()
        path1 = outDirPath + str(count)
        pygame.image.save(screen, path1 + '.png')

        costMatrix = general.creatCostMatrix(d, [])
        start_pos = general.find_start(d)
        end_pos = maze.get_goal_pos()
        # print(end_pos)

        params = [maze.get_score_data(), heuristic.calcPrefixSum(d)]

        # if level >= 2:

        # print(params)

        start_time = timer()

        if h == '4':
            cost, route = general.get_func_dict(alg_name, d, start_pos, end_pos, costMatrix, myMaze, d, h, params
                                                )
        elif h == '1':
            # print('params[0]: ', [params[0]])
            cost, route = general.get_func_dict(alg_name, d, start_pos, end_pos, costMatrix, myMaze, [params[0]]
                                                )
            print(route)

        else:
            cost, route = general.get_func_dict(alg_name, d, start_pos, end_pos, costMatrix, myMaze, params
                                                )
        # print(end_pos)
        type_trace = Cell.PATH
        if cost == general.G_MAX:
            type_trace = Cell.NOPATH
        end_time = timer()
        general.write_output_txt(path + '.txt', [], end_time - start_time, cost, route)
        count += 1
        # print(count, end_time - start_time)
        myMaze.trace_back(route, type_trace)
        alg_name1 = alg_name

        if h != '':
            alg_name1 += 'heuristic_' + str(h)
        pygame.image.save(screen, path1 + '/' + alg_name + '/' + alg_name1 + '.png')

        for i in range(50):
            recorder.capture_frame(screen)
        pg.quit()
        recorder.end_recording()


def advanced_main(alg_name, h=''):
    dirPath = 'input/advance'
    advanced_file_list = general.get_files(dirPath)
    # print(len(advanced_file_list))
    myMazeData = []
    teleportData = []
    for f in advanced_file_list:
        x, y = teleport.read_file_teleport(dirPath + '/' + f)
        # print(x, y)
        teleportData.append(x)
        myMazeData.append(y)
    # print(teleportData[0])
    outDirPath = 'output/advance/advance'
    count = 0
    for maze in myMazeData:
        path = record_change_output(outDirPath, alg_name, count + 1, h)
        d = np.array(maze.get_data())
        screen = pg.display.set_mode((1000, 500))
        screen.fill("White")
        myMaze = Maze((900, 450), d, screen)

        path1 = outDirPath + str(count + 1)
        pygame.image.save(screen, outDirPath + str(count + 1) + '.png')
        costMatrix = general.creatCostMatrix(d, [])
        # print(costMatrix)
        start_pos = general.find_start(d)
        end_pos = maze.get_goal_pos()

        myMaze.display()
        pygame.display.flip()
        params = [maze.get_score_data(), heuristic.calcPrefixSum(d)]
        start_time = timer()
        cntMatrix, cost, route = (None, None, None)
        if h == '4':
            cntMatrix, cost, route = general.get_func_dict(alg_name, d, start_pos, end_pos, costMatrix, myMaze, (d,
                                                                                                                 teleportData[
                                                                                                                     count],
                                                                                                                 h),
                                                           )
        elif h == '1':
            cntMatrix, cost, route = general.get_func_dict(alg_name, d, start_pos, end_pos, costMatrix, myMaze,
                                                           ([params[0]],
                                                            teleportData[
                                                                count]),
                                                           )
        else:
            cntMatrix, cost, route = general.get_func_dict(alg_name, d, start_pos, end_pos, costMatrix, myMaze, (params,
                                                                                                                 teleportData[
                                                                                                                     count])
                                                           )

        type_trace = Cell.PATH
        if cost == general.G_MAX:
            type_trace = Cell.NOPATH
        end_time = timer()
        general.write_output_txt(path + '.txt', [], end_time - start_time, cost, route)
        count += 1
        # print(count, end_time - start_time)
        myMaze.trace_back(route, type_trace)
        alg_name1 = alg_name
        if h != '':
            alg_name1 = alg_name + 'heuristic_' + str(h)
        pygame.image.save(screen, path1 + '/' + alg_name + alg_name1 + '.png')

        for i in range(50):
            recorder.capture_frame(screen)
        pg.quit()
        recorder.end_recording()
