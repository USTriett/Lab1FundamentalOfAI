import general


class MazeData:

    def __init__(self, num_score, score_data, data, goal_pos):
        self.__num_score = num_score
        self.__score_data = score_data.copy()
        self.__data = data.copy()
        self.__goal_pos = goal_pos

    def get_goal_pos(self):
        return self.__goal_pos

    def get_data(self):
        return self.__data

    def get_score_data(self):
        return self.__score_data


def read_data(file_name):
    with open(file_name, 'r') as file:
        if file.readable():
            num_score = file.readline()
            # print('num score ', num_score)
            score_data = []
            for i in range(int(num_score)):
                tup = tuple(file.readline()[0:-1].split(' '))
                integer_tuple = tuple(map(int, tup))
                score_data.insert(len(score_data), integer_tuple)
            # print(score_data)
            data = []
            while True:
                lines = file.readline().rstrip('\n')
                # print(lines)
                if not lines:
                    break
                lines = list(lines)

                data.insert(len(data), lines)
            (i, j) = general.find_end(data)
            data[i][j] = 'G'
            # print(i, j)
            goal_pos = [i, j]

    file.close()
    return MazeData(num_score, score_data, data, goal_pos)
