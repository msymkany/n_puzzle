import pandas as pd
from moves import moves

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
        self.heuristic = heuristic
        self.f_calculation = f_calculation
        self.comp_in_time = 0

    def a_star(self):
        while self.states['is_open_list'].sum():
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
                f = self.f_calculation(g, self.heuristic.get_h(i, self.solved_puzzle))
                if str(i) in self.states.index:
                    if f < self.states.loc[str(i)]['f']:
                        self.states.loc[str(i)] = [i, current.name, g, f, 1]
                else:
                    self.states.loc[str(i)] = [i, current.name, g, f, 1]
                if str(i) == self.solved_puzzle_hash:
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
