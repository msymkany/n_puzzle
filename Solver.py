from State import State

class Solver:

    def __init__(self, puzzle, psize, target, heuristic):
        # self.initial_puzzle = puzzle
        self.solved_puzzle = target
        self.psize = psize
        self.closed_list = {}
        self.opened_list = {str(puzzle): State(puzzle, None, heuristic.get_h(puzzle, target))}
        self.heuristic = heuristic

    def a_star(self):
        # while self.opened_list:
            
        pass

