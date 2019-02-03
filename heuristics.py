# class Heuristic():
from itertools import product

class Manhattan():

    def __init__(self, size):
        self.dist_map = self.get_distance(size)
        self.size = size
        self.len = size * size

    def get_h(self, puzzle, solved):
        all_h = [self.dist_map[num][solved.index(puzzle[num])]
                 for num in range(self.len)]
        return sum(all_h)

    def get_distance_one_num(self, row, col):
        return [abs(t_row - row) + abs(t_col - col)
                    for t_row, t_col in product(range(self.size), range(self.size))]

    @staticmethod
    def get_distance(self):
        d_map = {((row * self.size) + col) : self.get_distance_one_num(self.size, row, col)
                 for row, col in product(range(self.size), range(self.size))}
        return d_map
