import sys
from argparse import ArgumentParser, FileType
import os
import shlex
from my_error import MyError
from itertools import chain


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

                # Check if puzzle == solved puzzle later on
                # if len(set(puzzle)) != len(puzzle):
                #     raise MyError('Puzzle has duplicate values')
                #
                # print(puzzle)
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
    group.add_argument('-f', '--file', type=validate_input)
    group.add_argument('-g', '--generate', type=(lambda x: int(x) if int(x) > 3 else 3),
                        help="Size of the puzzle's side. Must be >= 3, otherwise defaults to 3",
                        dest="puzzle_size", default=3, required=False)
    parser.add_argument('-e', '--heuristic', type=int,
                        choices=[1, 2, 3], action="store",
                        dest="heuristic", default=1)
    return parser.parse_args()


def parse_input():
    args = parse_arguments()
    print(vars(args)) #tst


def main():
    parse_input()


if __name__ == "__main__":
    main()