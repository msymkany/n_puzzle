class Solver:

    def __init__(self, puzzle, psize, target):
        self.initial_puzzle = puzzle
        self.solved_puzzle = target
        self.psize = psize
        self.closed_list = []
        self.opened_list = {}
