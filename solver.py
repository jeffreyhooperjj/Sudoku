from typing import Iterable
import datetime
class SudokuSolver():
    def __init__(self, start_state: Iterable[int]):
        self.start_state = start_state
        self.potential_solution = start_state
        self.potential_vals = {}
        for i in range(len(start_state)):
            if self.potential_solution[i] != 0:
                self.potential_vals[i] = None
            else:
                self.potential_vals[i] = []
                for j in range(1, 10):
                    if self.can_put_in_row(i, j) and self.can_put_in_col(i, j) and self.can_put_in_grid(i, j):
                        self.potential_vals[i].append(j)
        self.constraint_checker()
        self.update_constraint_checker()

    def update_constraint_checker(self):
        for i in range(len(self.potential_solution)):
            if self.potential_vals[i] != None:
                for val in self.potential_vals[i]:
                    if not (self.can_put_in_row(i, val) and self.can_put_in_col(i, val) and self.can_put_in_grid(i, val)):
                        self.potential_vals[i].remove(val)
    def constraint_checker(self):
        for i in range(len(self.start_state)):
            if self.potential_vals[i] != None:
                if len(self.potential_vals[i]) == 1:
                    self.potential_solution[i] = self.potential_vals[i][0]
                    self.potential_vals[i] = None
    # param: 1x81 array filled with numbers 1-9
    def verify_solution(self, potential_solution: Iterable[int]) -> bool:
        # check that puzzle is filled
        # check that each row contains 1-9 once
        if len(potential_solution) != 81:
            print("Not a Sudoku puzzle")
            return False
        for i in range(len(potential_solution)):
            if potential_solution[i] < 1 or potential_solution[i] > 9:
                # print("Not a Sudoku solution")
                # self.print_puzzle(potential_solution)
                return False
        LENGTH = 9
        row = []
        for i in range(len(potential_solution)):
            row.append(potential_solution[i])
            if len(row) == LENGTH:
                if self.check_row(row) == False:
                    return False
                row = []
        # check that each column contains 1-9 once
        col = []
        for i in range(LENGTH):
            for j in range(LENGTH):
                cell = (j * LENGTH) + i
                col.append(potential_solution[cell])
            if self.check_col(col) == False:
                return False
            col = []
        # check that each 3x3 grid contains 1-9 once
        grid = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        cell = (27*i) + (3*j) + (k*LENGTH) + l
                        grid.append(potential_solution[cell])
                grid = []
        self.print_puzzle(potential_solution)
        print("Valid Solution")
        return True

    def check_row(self, row: Iterable[int]) -> bool:
        #initialize vals to 0
        count = {}
        for i in range(len(row)):
            count[i+1] = 0
        #count numbers in sudoku
        #TODO: add error checking if invalid puzzle
        for num in row:
            count[num] += 1
        for i in range(len(row)):
            if count[i+1] == 0 or count[i+1] > 1:
                print(f"Count {i+1} = {count[i+1]}\n{row}")
                return False
        return True
        
    def check_col(self, col: Iterable[int]) -> bool:
        # initialize all counts to 0
        return self.check_row(col)
    
    def check_grid(self, grid: Iterable[int]) -> bool:
         # initialize all counts to 0
        return self.check_row(grid)
    def print_puzzle(self, puzzle: Iterable[int]) -> None:
        for i in range(9):
            for j in range(9):
                cell = (i * 9) + j
                print(f"{puzzle[cell]}", end=" ")
            print("")
    def is_board_filled(self):
        for i in range(len(self.start_state)):
            if self.potential_solution[i] == 0:
                return False
        return True
    def find_empty_spot(self) -> int:
        for i in range(len(self.potential_solution)):
            if self.potential_solution[i] == 0:
                return i
        return -1

    def find_solutions(self) -> bool:
        # trivial as of right now

        # if self.is_board_filled():
        if self.verify_solution(self.potential_solution) == True:
            return True
        # else:
        #     return False
        else:
            pos = self.find_empty_spot()
            if self.is_available(pos) and self.potential_vals[pos] != None:
                for potential_val in self.potential_vals[pos]:
                    if self.is_valid_move(pos, potential_val):
                        self.potential_solution[pos] = potential_val
                        if self.find_solutions():
                            return True
                        self.potential_solution[pos] = 0
                    # potential_vals[pos].remove(potential_val)
                    # print(f"After: {potential_vals[pos]}")
            return False

    def is_available(self, pos: int) -> bool:
        return self.potential_solution[pos] == 0

    def is_valid_move(self, pos: int, num: int) -> bool:
        # check row
        # check col
        # check 3x3 square
        current_val = self.potential_solution[pos]
        # if self.potential_solution[pos] != 0:
            # return False
        return self.can_put_in_row(pos, num) and self.can_put_in_col(pos, num) and self.can_put_in_grid(pos, num)
    
    def can_put_in_row(self, pos: int, num: int) -> bool:
        row = pos // 9
        for i in range(row*9,row*9+9):
            if self.potential_solution[i] == num:
                return False
        return True
    
    def can_put_in_col(self, pos: int, num: int) -> bool:
        col = pos % 9
        for i in range(col, len(self.start_state), 9):
            if self.potential_solution[i] == num:
                return False
        return True
    
    def can_put_in_grid(self, pos: int, num: int) -> bool:
        col = pos % 9
        row = pos // 9
        grid = None
        if row < 3 and col < 3:
            grid = 1
        elif row < 3 and col < 6:
            grid = 2
        elif row < 3 and col <= 8:
            grid = 3
        elif row < 6 and col < 3:
            grid = 4
        elif row < 6 and col < 6:
            grid = 5
        elif row < 6 and col <= 8:
            grid = 6
        elif row <= 8 and col < 3:
            grid = 7
        elif row <= 8 and col < 6:
            grid = 8
        else:
            grid = 9
        start = None
        offset = None
        if grid < 4:
            start = 0
        elif grid < 7:
            start = 27
        else:
            start = 54
        if grid % 3 == 2:
            offset = 3
        elif grid % 3 == 0:
            offset = 6
        else:
            offset = 0

        for i in range(3):
            for j in range(3):
                cell = (start) + (offset) + (i*9) + j
                if self.potential_solution[cell] == num:
                    return False
        return True

import random
class SudokuGenerator():
    def __init__(self):
        self.puzzles = []
        self.puzzle_len = 81

    def generate_puzzles(self, num: int) -> []:
        for _ in range(num):
            puzzle = self.random_start_puzzle()
            self.puzzles.append(puzzle)
        for puzzle in self.puzzles:
            solver = SudokuSolver(puzzle)
            solver.find_solutions()
    def random_start_puzzle(self) -> []:
        puzzle = [0 for _ in range(self.puzzle_len)]
        for _ in range(3):
            pos = random.randint(0, self.puzzle_len - 1)
            number_into_sudoku_puzzle = random.randint(1, 9)
            puzzle[pos] = number_into_sudoku_puzzle
            while not (self.can_put_in_row(pos, number_into_sudoku_puzzle, puzzle) or self.can_put_in_col(pos, number_into_sudoku_puzzle, puzzle) or self.can_put_in_grid(pos, number_into_sudoku_puzzle, puzzle)):
                pos = random.randint(0, self.puzzle_len - 1)
                number_into_sudoku_puzzle = random.randint(1, 9)
                print(f"{pos} {number_into_sudoku_puzzle}")
        return puzzle
    def can_put_in_row(self, pos: int, num: int, puzzle: [int]) -> bool:
        row = pos // 9
        for i in range(row*9,row*9+9):
            if puzzle[i] == num:
                return False
        return True
    
    def can_put_in_col(self, pos: int, num: int, puzzle: [int]) -> bool:
        col = pos % 9
        for i in range(col, self.puzzle_len, 9):
            if puzzle[i] == num:
                return False
        return True
    
    def can_put_in_grid(self, pos: int, num: int, puzzle: [int]) -> bool:
        col = pos % 9
        row = pos // 9
        grid = None
        if row < 3 and col < 3:
            grid = 1
        elif row < 3 and col < 6:
            grid = 2
        elif row < 3 and col <= 8:
            grid = 3
        elif row < 6 and col < 3:
            grid = 4
        elif row < 6 and col < 6:
            grid = 5
        elif row < 6 and col <= 8:
            grid = 6
        elif row <= 8 and col < 3:
            grid = 7
        elif row <= 8 and col < 6:
            grid = 8
        else:
            grid = 9
        start = None
        offset = None
        if grid < 4:
            start = 0
        elif grid < 7:
            start = 27
        else:
            start = 54
        if grid % 3 == 2:
            offset = 3
        elif grid % 3 == 0:
            offset = 6
        else:
            offset = 0

        for i in range(3):
            for j in range(3):
                cell = (start) + (offset) + (i*9) + j
                if puzzle[cell] == num:
                    return False
        return True

if __name__ == "__main__":
    start_state = [0, 0, 0, 6, 0, 0, 4, 0, 0,
                   7, 0, 0, 0, 0, 3, 6, 0, 0,
                   0, 0, 0, 0, 9, 1, 0, 8, 2,
                   0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 5, 0, 1, 8, 0, 0, 0, 3,
                   0, 0, 0, 3, 0, 6, 0, 4, 5,
                   0, 4, 0, 2, 0, 0, 0, 6, 0,
                   9, 0, 3, 0, 0, 0, 0, 0, 0,
                   0, 2, 0, 0, 0, 0, 1, 0, 0]
    
    puzzle2 = [5, 8, 1, 0, 7, 2, 4, 3, 9,
              7, 9, 2, 8, 4, 3, 6, 5, 1,
              3, 6, 4, 5, 9, 1, 7, 8, 2,
              4, 3, 8, 9, 5, 7, 2, 1, 6,
              2, 5, 6, 1, 8, 4, 9, 7, 3,
              1, 7, 9, 3, 2, 6, 8, 4, 5,
              8, 4, 5, 2, 1, 9, 3, 6, 7,
              9, 1, 3, 7, 6, 8, 5, 2, 4,
              6, 2, 7, 4, 3, 5, 1, 9, 8]
    
    puzzle = [5, 8, 1, 6, 7, 2, 4, 3, 9,
              7, 9, 2, 8, 4, 3, 6, 5, 1,
              3, 6, 4, 5, 9, 1, 7, 8, 2,
              4, 3, 8, 9, 5, 7, 2, 1, 6,
              2, 5, 6, 1, 8, 4, 9, 7, 3,
              1, 7, 9, 3, 2, 6, 8, 4, 5,
              8, 4, 5, 2, 1, 9, 3, 6, 7,
              9, 1, 3, 7, 6, 8, 5, 2, 4,
              6, 2, 7, 4, 3, 5, 1, 9, 8]

    puzzle3 = [0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 6, 0, 0, 0, 0, 3,
               0, 0, 4, 0, 8, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 3, 0, 0, 2,
               0, 8, 0, 0, 4, 0, 0, 1, 0,
               6, 0, 0, 5, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 1, 0, 7, 8, 0,
               5, 0, 0, 0, 0, 9, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 4, 0]

    puzzle4 = [0, 3, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0,
               0, 0, 0, 0, 0, 0, 0, 0, 0]

    # solver = SudokuSolver(puzzle4)
    
    # # print(potential_vals)
    # start = datetime.datetime.now()
    # print("Solving Puzzle...")
    # solver.find_solutions()
    # print("Puzzle solved")
    # end = datetime.datetime.now()
    # print(f"Time to solve: {end - start}")

    generator = SudokuGenerator()
    generator.generate_puzzles(10)
