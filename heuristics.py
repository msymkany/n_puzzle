from itertools import product
from math import sqrt
import numpy as np


class Heuristic():

    def __init__(self, size):
        self.size = size
        self.len = size * size
        self.dist_map = 0

    def get_distance_one_num(self, row, col):
        pass

    def get_distance(self):
        d_map = {((row * self.size) + col) : self.get_distance_one_num(row, col)
                 for row, col in product(range(self.size), range(self.size))}
        return d_map

    def get_h(self, puzzle, solved):
        all_h = [self.dist_map[num][solved.index(puzzle[num])]
                 for num in range(self.len)]
#         print(all_h) #test
        return sum(all_h)


class Euclidian(Heuristic):

    def __init__(self, size):
        super().__init__(size)
        self.dist_map = self.get_distance()
        
    def get_distance_one_num(self, row, col):
        return [sqrt((t_row - row)**2 + (t_col - col)**2)
                    for t_row, t_col in product(range(self.size), range(self.size))]

    
class Manhattan(Heuristic):

    def __init__(self, size):
        super().__init__(size)
        self.dist_map = self.get_distance()
        
    def get_distance_one_num(self, row, col):
        return [abs(t_row - row) + abs(t_col - col)
                    for t_row, t_col in product(range(self.size), range(self.size))]

    
class Hamming(Heuristic):

    def __init__(self, size):
        super().__init__(size)
        
    def get_h(self, puzzle, solved):
        return np.count_nonzero(np.array(puzzle) - np.array(solved))


heuristics = [Manhattan, Euclidian, Hamming]
