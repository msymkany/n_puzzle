def move_up(puzzle, hole, psize):
    if hole + 1 > psize:
        new = puzzle[:]
        new[hole], new[hole - psize] = new[hole - psize], new[hole]
        return new


def move_down(puzzle, hole, psize):
    if hole + 1 + psize <= psize * psize:
        new = puzzle[:]
        new[hole], new[hole + psize] = new[hole + psize], new[hole]
        return new


def move_left(puzzle, hole, psize):
    if (hole) % psize:
        new = puzzle[:]
        new[hole], new[hole - 1] = new[hole - 1], new[hole]
        return new


def move_right(puzzle, hole, psize):
    if (hole + 1) % psize:
        new = puzzle[:]
        new[hole], new[hole + 1] = new[hole + 1], new[hole]
        return new


moves = [move_up, move_down, move_left, move_right]