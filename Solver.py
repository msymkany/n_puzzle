import pandas as pd
import numpy as np
from moves import moves
import sys

# class Solver:

#     def __init__(self, puzzle, psize, target, 
#                 heuristic, f_calculation):
#         self.initial = puzzle
#         self.solved_puzzle_hash = str(target)
#         self.solved_puzzle = target
#         self.psize = psize
#         self.open = pd.DataFrame({'puzzle': [puzzle], 'parent': None, 'g': 0,
#                                     'f': heuristic.get_h(puzzle, target)},
#                                    index=[(str(puzzle))])
#         self.closed = self.open.copy(deep=True)
#         self.heuristic = heuristic
#         self.f_calculation = f_calculation
#         self.comp_in_time = 0

#     def a_star(self):
#         if self.closed.iloc[0].name == self.solved_puzzle_hash:
#                 return self.get_result(self.closed.iloc[0])
#         while not self.open.empty:
#             current = self.open.iloc[0]
#             self.closed.loc[current.name] = current.values
#             # else:
#             self.comp_in_time += 1
#             self.open.drop(current.name)
#             # self.states.loc[current.name, 'is_open_list'] = 0
#             self.expand(current)
#             self.open = self.open.sort_values('f')


#     def expand(self, current):
#         hole_index = current.puzzle.index(0)
#         expanded = [foo(current.puzzle, hole_index, self.psize) for foo in moves]
#         g = current.g + 1
#         for i in expanded:
#             if i:
#                 str_i = str(i)
#                 if str_i == self.solved_puzzle_hash:
#                     self.closed.loc[str_i] = [i, current.name, g, g]
#                     return self.get_result(self.closed.loc[str_i])
#                 f = self.f_calculation(g, self.heuristic.get_h(i, self.solved_puzzle))
#                 if str_i in self.open.index:
#                     if f < self.open.loc[str_i]['f']:
#                         self.open.loc[str_i] = [i, current.name, g, f]
#                 elif str_i in self.closed.index:
#                     if f < self.closed.loc[str_i]['f']:
#                         self.open.loc[str_i] = [i, current.name, g, f]
#                         self.closed.drop(current.name)
#                 else:
#                     self.open.loc[str_i] = [i, current.name, g, f]
                

#     def print_states(self, idx, size):
#         if self.closed.loc[idx, 'parent']:
#             self.print_states(self.closed.loc[idx, 'parent'], size)
#         print('step ', self.closed.loc[idx, 'g'])
#         chunks = (self.closed.loc[idx, 'puzzle'][i : i + size]
#                for i in range(0, size*size, size))
#         for ch in chunks:
#             print(ch)

#     def get_result(self, current):
#         print('Complexity in time: ', self.comp_in_time)
#         print('Complexity in space: ', self.closed.shape[0])
#         print('Number of moves to solve puzzle: ', current.g)
#         self.print_states(current.name, self.psize)
#         sys.exit()

class Solver:

    def __init__(self, puzzle, psize, target, 
                heuristic, f_calculation):
        self.initial = puzzle
        self.solved_puzzle_hash = str(target)
        self.solved_puzzle = target
        self.psize = psize
        self.states = pd.DataFrame({'puzzle': [puzzle], 'parent': None, 'g': 0,
                                    'f': heuristic.get_h(puzzle, target), 'is_open_list': 1},
                                   index=[(str(puzzle))])
        # fff = self.states['f'].idxmin(axis =1)
        # fff = np.argmin(self.states[self.states.is_open_list == 1].f.values)

        # print(self.states.f.values.idxmin())
        # print(fff)
        # print(heuristic.get_h(puzzle, target))
        self.heuristic = heuristic
        self.f_calculation = f_calculation
        self.comp_in_time = 0

    def a_star(self):
        # print(self.states.f.idxmin())
        while self.states['is_open_list'].sum():
            # current = self.states.iloc[np.argmin(self.states[self.states.is_open_list == 1].f.values)]
            # current = self.states[self.states.is_open_list == 1].iloc[self.states.f.idxmin()]
            current = self.states[self.states.is_open_list == 1].iloc[0]
            if current.name == self.solved_puzzle_hash:
                return self.get_result(current)
            else:
                self.comp_in_time += 1
                self.states.loc[current.name, 'is_open_list'] = 0
                self.expand(current)
                self.states = self.states.sort_values('f')


    def expand(self, current):
        hole_index = current.puzzle.index(0)
        expanded = [foo(current.puzzle, hole_index, self.psize) for foo in moves]
        g = current.g + 1
        for i in expanded:
            if i:
                str_i = str(i)
                f = self.f_calculation(g, self.heuristic.get_h(i, self.solved_puzzle))
                # print(f)
                if str_i in self.states.index:
                    if f < self.states.loc[str_i]['f']:
                        self.states.loc[str_i] = [i, current.name, g, f, 1]
                else:
                    self.states.loc[str_i] = [i, current.name, g, f, 1]
                if str_i == self.solved_puzzle_hash:
                    return

    def print_states(self, idx, size):
        if self.states.loc[idx, 'parent']:
            self.print_states(self.states.loc[idx, 'parent'], size)
        print('step ', self.states.loc[idx, 'g'])
        chunks = (self.states.loc[idx, 'puzzle'][i : i + size]
               for i in range(0, size*size, size))
        for ch in chunks:
            print(ch)

    def get_result(self, current):
        print('Complexity in time: ', self.comp_in_time)
        print('Complexity in space: ', self.states.shape[0])
        print('Number of moves to solve puzzle: ', current.g)
        self.print_states(current.name, self.psize)