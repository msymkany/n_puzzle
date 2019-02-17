# import sys
from argparse import ArgumentParser
import os
import shlex
from my_error import MyError
from itertools import chain
import random
from Solver import Solver
from heuristics import heuristics

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
    except FileNotFoundError:
        print("File not found")
    except IsADirectoryError:
        print("Is a directory")
    except PermissionError:
        print("Don't have permission to read a file")
    except IOError:
        print("Fail to read the file")
    except ValueError:
        print("No puzzle in file")
    except MyError as error:
        print(error.value)


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
                        dest="iterations", default=1000)
    return parser.parse_args()


def parse_input():
    args = vars(parse_arguments())
    # print(args) #tst
    if args['puzzle']:
        args['puzzle_size'] = args['puzzle'][0]
        args['puzzle'] = args['puzzle'][1]
        
    print(args) #tst
    return (args)
    
#Your functions here
#     else:
#         args['puzzle'] = generate_puzzle(args['puzzle_size'])
    
#     args['solved'] = make_solved_puzzle(args['puzzle_size'])
# # Check if sorted puzzle == solved puzzle
#     try:    
#         if (set(args['puzzle'])) != set(args['solved']):
#             raise MyError('Invalid puzzle')
#     except MyError as error:
#         print(error.value)
#     check_if_puzzle_is_solvable(args['puzzle'])
    
#1 2 3 4 12 13 14 5 11 0 15 6 10 9 8 7

def generate_puzzle(a, iters):
    p = make_solved_puzzle(a)
    # p[2 * a + 0] = 0
    # p[9] = 30
    size = a - 1
    row = 0
    row_0 = -1
    col_0 = -1
    row_1 = -1
    col_1 = -1
    #find coord of 0
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
        #random 0 - left, 1 - up, 2 - right, 3 - down
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

def check_if_puzzle_is_solvable(a, p):
    inver = 0
    size = a - 1

    i = 0
    while p[i] != 0:
        i += 1
    p[i] = a * a

    i = 0
    while i < (a * a):
        j = i
        while j < (a * a):
            if (p[j] < p[i]):
                inver += 1
            j += 1
        i += 1
    if inver % 2 == 0:
        return 0
    else:
        return 1

# def check_if_puzzle_is_solvable(a, p):
#     inver = 0
#     size = a - 1
#
#     pos = -1
#
#     row_t = 0
#     col_t = -1
#     way_row_t = 0
#     way_col_t = 1
#     step_t = 1
#     zone00_t = 0
#     zone01_t = 0
#     zone11_t = 0
#     zone10_t = 0
#     while step_t < a * a:
#         row_t += way_row_t
#         col_t += way_col_t
#         if (row_t == (zone00_t) and col_t == zone00_t - 1): # 0 0
#             way_row_t = 0
#             way_col_t = 1
#             zone10_t += 1
#         elif (col_t == (size - zone01_t) and row_t == (0 + zone01_t)): # 0 1
#             way_row_t = 1
#             way_col_t = 0
#             zone00_t += 1
#         elif (row_t == (size - zone11_t) and col_t == (size - zone11_t)): # 1 1
#             way_row_t = 0
#             way_col_t = -1
#             zone01_t += 1
#         elif (col_t == (zone10_t) and row_t == (size - zone10_t)): # 1 0
#             way_row_t = -1
#             way_col_t = 0
#             zone11_t += 1
#         step_t += 1
#
#         row = 0
#         col = -1
#         way_row = 0
#         way_col = 1
#         step = 1
#         zone00 = 0
#         zone01 = 0
#         zone11 = 0
#         zone10 = 0
#         if (pos == -1 and p[row_t * a + col_t] == 0):
#             pos = step_t
#         while step <= a * a:
#             row += way_row
#             col += way_col
#             if (p[row * a + col] < p[row_t * a + col_t]) and p[row * a + col] != 0:
#                 inver += 1
#             if (row == (zone00) and col == zone00 - 1): # 0 0
#                 way_row = 0
#                 way_col = 1
#                 zone10 += 1
#             elif (col == (size - zone01) and row == (0 + zone01)): # 0 1
#                 way_row = 1
#                 way_col = 0
#                 zone00 += 1
#             elif (row == (size - zone11) and col == (size - zone11)): # 1 1
#                 way_row = 0
#                 way_col = -1
#                 zone01 += 1
#             elif (col == (zone10) and row == (size - zone10)): # 1 0
#                 way_row = -1
#                 way_col = 0
#                 zone11 += 1
#             step += 1
#         p[row_t * a + col_t] = 0
#     pos = int(pos / a)
#     print(inver)
#     print(pos)
#     if a % 2 != 0 and inver % 2 == 0:
#         return (1)
#     elif a % 2 == 0:
#         if pos % 2 != 0 and inver % 2 != 0:
#             return (1)
#         elif pos % 2 == 0 and inver % 2 == 0:
#             return (1)
#     return (0)


def main():
    args = parse_input()
    if (not args['puzzle']):
        args['puzzle'] = generate_puzzle(args['puzzle_size'], args['iterations'])
    args['solved'] = make_solved_puzzle(args['puzzle_size'])
    print(args) # tst

# # Check if sorted puzzle == solved puzzle
    try:    
        if (set(args['puzzle'])) != set(args['solved']):
            raise MyError('Invalid puzzle')
        if not (check_if_puzzle_is_solvable(args['puzzle_size'], args['puzzle'])):
            raise MyError('The puzzle is unsolvable')
    #     print("gogogo")
    except MyError as error:
        print(error.value)
    # if (check_if_puzzle_is_solvable(args['puzzle_size'], args['puzzle'])):
    #     print("gogogo")
    # else:
    #     print("Sad")
    solv = Solver(args['puzzle'], args['puzzle_size'], args['solved'],
                  heuristics[args['heuristic'] - 1](args['puzzle_size']))
    solv.a_star()

if __name__ == "__main__":
    main()
