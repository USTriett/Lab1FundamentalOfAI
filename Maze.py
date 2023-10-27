from idlelib.pyshell import eof

import pygame as pg
import pygame.event
from sys import exit
import numpy as np
from enum import Enum
import maze_data as md


# print(1)

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

    def __init__(self, size_screen, data):

        self.color_map = {Cell.EMPTY: "White", Cell.PATH: "Yellow", Cell.GOAL: "Red", Cell.BLOCKED: "Black", Cell.START: "Green"}
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

    def update_cell(self, pos):
        # print(self.__data[pos[0]][pos[1]])
        self.__color_pos__(pos[0], pos[1], self.color_map[self.__data[pos[0]][pos[1]]])

        return self.__data[pos[0]][pos[1]]

    def trace_back(self, pos):
        cost = 0
        for [i, j] in pos:
            cost += self.update_cell([i, j])
        return cost

    def display(self, main_screen):
        main_screen.blit(self.__screen, (0, 0))

    def generate_maze(self, file_name):
        pass


if __name__ == "__main__":
    # print(1)
    myMazeData = md.read_data("maze_map.txt")
    d = np.array(myMazeData.get_data())
    # print(d[1])
    pg.init()
    screen = pg.display.set_mode((1000, 500))
    screen.fill("White")
    myMaze = Maze((900, 450), d)
    myMaze.display(screen)
    pygame.display.flip()
    running = True
    while running:
        # m.display()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()


# pg.init()
# main_screen = pg.display.set_mode((800, 400))
# main_screen.fill("White")
# running = True
#
# m = Maze((600, 300), d)
# m.update_cell([2, 2])
#
# pygame.display.flip()
# while running:
#     m.display()
#     pygame.display.flip()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
# pygame.quit()
