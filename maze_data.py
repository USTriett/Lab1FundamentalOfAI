import general

class MazeData:
    def __init__(self, num_score, score_data, data):
        self.__num_score = num_score
        self.__score_data = score_data.copy()
        self.__data = data.copy()

    def get_data(self):
        return self.__data


def read_data(file_name):
    with open(file_name, 'r') as file:
        if file.readable():
            num_score = file.readline(2)
            # print(num_score)
            score_data = []
            for i in range(int(num_score)):
                tup = file.readline().split(' ')
                for j in tup:
                    score_data.insert(len(score_data), int(j))
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
    file.close()
    return MazeData(num_score, score_data, data)