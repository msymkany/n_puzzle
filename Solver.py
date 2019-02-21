import pandas as pd
import numpy as np
from moves import moves
import sys
import bisect

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
        self.open_f = [self.states.f[0]]
        self.open_idx = [(str(puzzle))]
        
        
#         print(self.open_f)
#         print(self.open_idx)
        # print(heuristic.get_h(puzzle, target))
        self.heuristic = heuristic
        self.f_calculation = f_calculation
        self.comp_in_time = 0

    def a_star(self):
        if self.states.iloc[0].name == self.solved_puzzle_hash:
                return self.get_result(self.states.iloc[0])
        while self.states['is_open_list'].sum():
#             current = self.states.iloc[np.argmin(self.states[self.states.is_open_list == 1].f.values)]
#             current = self.states.loc[self.states[self.states.is_open_list == 1].f.idxmin()]
#             current = self.states[self.states.is_open_list == 1].iloc[0]
            current = self.states.loc[self.open_idx.pop(0)]
            self.open_f.pop(0)
#             else:
            self.comp_in_time += 1
            self.states.loc[current.name, 'is_open_list'] = 0
            self.expand(current)
#                 self.states = self.states.sort_values('f')


    def expand(self, current):
        hole_index = current.puzzle.index(0)
        expanded = [foo(current.puzzle, hole_index, self.psize) for foo in moves]
        g = current.g + 1
        for i in expanded:
            if i:
                str_i = str(i)
                if str_i == self.solved_puzzle_hash:
#                     print('finita')
                    self.states.loc[str_i] = [i, current.name, g, g, 1]
                    return self.get_result(self.states.loc[str_i])
                f = self.f_calculation(g, self.heuristic.get_h(i, self.solved_puzzle))
                # print(f)
                if str_i in self.states.index:
                    if f < self.states.loc[str_i]['f']:
                        self.states.loc[str_i] = [i, current.name, g, f, 1]
                        self.open_idx.insert(bisect.bisect_left(self.open_f, f), str_i)
                        bisect.insort_left(self.open_f, f)
#                         print(self.open_f)
#                         print(self.open_idx)
                else:
                    self.states.loc[str_i] = [i, current.name, g, f, 1]
                    self.open_idx.insert(bisect.bisect_left(self.open_f, f), str_i)
                    bisect.insort_left(self.open_f, f)
#                     print(self.open_f)
#                     print(self.open_idx)
                

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
        sys.exit()