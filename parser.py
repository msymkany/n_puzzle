import sys
from argparse import ArgumentParser
import os
import shlex
from my_error import MyError
from itertools import chain
import random
from Solver import Solver
from heuristics import heuristics
from is_solvable import check_if_puzzle_is_solvable

args = 0
def check_int(num):
    try:
        return int(num)
    except ValueError:
        print('Invalid number in puzzle: ', num)


def validate_input(filename):
    try:
        if os.path.getsize(filename) > 0:
            with open(filename, 'r') as file:
                text = file.readlines()
                lines = [list(shlex.shlex(item)) for item in text if list(shlex.shlex(item))]
                if not lines:
                    raise ValueError()
                if len(lines) < 4:
                    raise MyError('Invalid puzzle')
                if len(lines[0]) != 1:
                    raise MyError('Invalid puzzle size')
                psize = check_int(lines[0][0])
                if len(lines) != psize + 1:
                    raise MyError('Puzzle height mismatch')
                puzzle_form = (len(l) for l in lines[1:])
                for i in puzzle_form:
                    if i != psize:
                        raise MyError('Puzzle column length mismatch')
                puzzle = list(chain(*lines[1:]))
                puzzle = [check_int(i) for i in puzzle]
                return psize, puzzle
        else:
            raise EOFError
    except EOFError:
        print("Empty file")
        sys.exit()
    except FileNotFoundError:
        print("File not found")
        sys.exit()
    except IsADirectoryError:
        print("Is a directory")
        sys.exit()
    except PermissionError:
        print("Don't have permission to read a file")
        sys.exit()
    except IOError:
        print("Fail to read the file")
        sys.exit()
    except ValueError:
        print("No puzzle in file")
        sys.exit()
    except MyError as error:
        print(error.value)
        sys.exit()

def parse_arguments():
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--puzzle', type=validate_input)
    group.add_argument('-g', '--generate', type=(lambda x: int(x) if int(x) >= 3 else 3),
                        help="Size of the puzzle's side. Must be >= 3, otherwise defaults to 3",
                        dest="puzzle_size")
    parser.add_argument('-e', '--heuristic', type=int,
                        choices=[1, 2, 3], action="store",
                        dest="heuristic", default=1)
    parser.add_argument('-i', '--iterations', type=int,
                        action="store",
                        dest="iterations", default=31)
    parser.add_argument('-c', '--coefficient', type=int,
                        action="store",
                        dest="coefficient", default=1)
    return parser.parse_args()


def parse_input():
    args = vars(parse_arguments())
    if args['puzzle']:
        args['puzzle_size'] = args['puzzle'][0]
        args['puzzle'] = args['puzzle'][1]
        
    return (args)

def generate_puzzle(a, iters):
    p = make_solved_puzzle(a)
    size = a - 1
    row = 0
    row_0 = -1
    col_0 = -1
    row_1 = -1
    col_1 = -1
    while (row < a and row_0 == -1):
        col = 0
        while (col < a and row_0 == -1):
            if (p[row * a + col] == 0):
                row_0 = row
                col_0 = col
            col += 1
        row += 1
    it = 0
    while (it < iters):
        r1 = [0, 1, 2, 3]
        if (row_0 == 0 and col_0 == 0):         # 0 0
            r1 = [2, 3]                         #23
        elif (row_0 == 0 and col_0 == size):    # 0 1
            r1 = [0, 3]                         #03
        elif (row_0 == 0):                      # 00 - 01
            r1 = [0, 2, 3]                      #023
        elif (row_0 == size and col_0 == size): # 1 1
            r1 = [0, 1]                         #01
        elif (col_0 == size):                   # 01 - 11
            r1 = [0, 1, 3]                      #013
        elif (row_0 == size and col_0 == 0):    # 1 0
            r1 = [1, 2]                         #12
        elif (row_0 == size):                   # 11 - 10
            r1 = [0, 1, 2]                      #012
        elif (col_0 == 0 and row_0 > 0 and row_0 < size): # 10 - 00
            r1 = [1, 2, 3]                      #123
        ra = random.choice(r1)
        if (ra == 0):
            row_1 = 0
            col_1 = -1
        elif (ra == 1):
            row_1 = -1
            col_1 = 0
        elif (ra == 2):
            row_1 = 0
            col_1 = 1
        elif (ra == 3):
            row_1 = 1
            col_1 = 0
        num_tmp = p[(row_0 + row_1) * a + (col_0 + col_1)]
        p[(row_0 + row_1) * a + (col_0 + col_1)] = 0
        p[row_0 * a + col_0] = num_tmp
        row_0 = row_0 + row_1
        col_0 = col_0 + col_1
        it += 1
    return (p)

def make_solved_puzzle(a):
    p = [0] * a * a
    size = a - 1
    row = 0
    col = -1
    way_row = 0
    way_col = 1
    step = 1
    zone00 = 0
    zone01 = 0
    zone11 = 0
    zone10 = 0
    while step < a * a:
        row += way_row
        col += way_col
        p[row * a + col] = step
        if (row == (zone00) and col == zone00 - 1): # 0 0
            way_row = 0
            way_col = 1
            zone10 += 1
        elif (col == (size - zone01) and row == (0 + zone01)): # 0 1
            way_row = 1
            way_col = 0
            zone00 += 1
        elif (row == (size - zone11) and col == (size - zone11)): # 1 1
            way_row = 0
            way_col = -1
            zone01 += 1
        elif (col == (zone10) and row == (size - zone10)): # 1 0
            way_row = -1
            way_col = 0
            zone11 += 1
        step += 1
    return (p)

def main():
    args = parse_input()
    if (not args['puzzle']):
        args['puzzle'] = generate_puzzle(args['puzzle_size'], args['iterations'])
    args['solved'] = make_solved_puzzle(args['puzzle_size'])

    try:    
        if (set(args['puzzle'])) != set(args['solved']):
            raise MyError('Invalid puzzle')
        if not (check_if_puzzle_is_solvable(args['puzzle_size'], args['puzzle'][:], args['solved'][:])):
            raise MyError('The puzzle is unsolvable')
    except MyError as error:
        print(error.value)
        return()
    solv = Solver(args['puzzle'], args['puzzle_size'], args['solved'],
                  heuristics[args['heuristic'] - 1](args['puzzle_size']),
                   f_calculation =(lambda g, h: g + h * (args['coefficient'])))
    solv.a_star()


if __name__ == "__main__":
    main()
