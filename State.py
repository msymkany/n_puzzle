class State:

    def __init__(self, puzzle, parent, g, f):
        self.state = puzzle
        self.parent = parent
        self.g = g
        self.f = f

