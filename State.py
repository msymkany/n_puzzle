class State:

    def __init__(self, puzzle, parent, f):
        self.state = puzzle
        self.parent = parent
        self.f = f

