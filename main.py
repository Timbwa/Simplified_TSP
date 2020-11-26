#import numpy as np


class Map:
    def __init__(self, file_name):
        self.__map = []
        self.__file_name = file_name
        self.__read_map(self.__file_name)

    def get_file_name(self):
        return self.__file_name

    def get_map(self):
        return self.__map

    def __read_map(self, file_name):
        with open(file_name, 'r') as f:
            for line in f:
                self.__map.append([el for index, el in enumerate(line.rstrip('\n'))])


if __name__ == "__main__":
    # represent map / puzzle as 2D array
    map_obj = Map("map.txt")
    print(len(map_obj.get_map()))




