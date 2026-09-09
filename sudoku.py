"""Core Sudoku data and rules for the terminal game."""

from copy import deepcopy
import random
from typing import List, Optional, Tuple

Board = List[List[int]]
Position = Tuple[int, int]

# A solved board gives every puzzle a known, valid answer.
SOLVED_BOARD: Board = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]

# Each puzzle starts with the same solution but has a different clue pattern.
PUZZLES = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ],
    [
        [5, 0, 0, 6, 0, 0, 9, 0, 0],
        [0, 7, 2, 0, 9, 0, 0, 4, 0],
        [0, 0, 8, 3, 0, 0, 0, 0, 7],
        [8, 0, 0, 0, 6, 0, 4, 0, 0],
        [0, 2, 6, 8, 0, 3, 0, 0, 0],
        [0, 0, 3, 0, 2, 0, 8, 5, 0],
        [9, 0, 0, 5, 0, 7, 2, 0, 0],
        [0, 8, 0, 0, 1, 0, 6, 3, 0],
        [0, 0, 5, 0, 8, 6, 0, 0, 9],
    ],
]

DIFFICULTY_REMOVALS = {"easy": 0, "medium": 8, "hard": 18}


def copy_board(board: Board) -> Board:
    """Return a separate copy so the original puzzle stays protected."""
    return deepcopy(board)


def is_valid_move(board: Board, row: int, column: int, number: int) -> bool:
    """Check whether number can be placed at zero-based row and column."""
    if not (0 <= row < 9 and 0 <= column < 9 and 1 <= number <= 9):
        return False

    for current_column in range(9):
        if current_column != column and board[row][current_column] == number:
            return False

    for current_row in range(9):
        if current_row != row and board[current_row][column] == number:
            return False

    box_row = (row // 3) * 3
    box_column = (column // 3) * 3
    for current_row in range(box_row, box_row + 3):
        for current_column in range(box_column, box_column + 3):
            if (current_row, current_column) != (row, column):
                if board[current_row][current_column] == number:
                    return False
    return True


def is_fixed_cell(original_board: Board, row: int, column: int) -> bool:
    """Return True when the original puzzle contains a clue in this cell."""
    return original_board[row][column] != 0


def is_valid_solution(board: Board) -> bool:
    """Return True only when the board is a completely valid Sudoku."""
    if len(board) != 9 or any(len(row) != 9 for row in board):
        return False
    if any(cell < 1 or cell > 9 for row in board for cell in row):
        return False

    for index in range(9):
        if set(board[index]) != set(range(1, 10)):
            return False
        if {board[row][index] for row in range(9)} != set(range(1, 10)):
            return False

    for box_row in range(0, 9, 3):
        for box_column in range(0, 9, 3):
            values = [
                board[row][column]
                for row in range(box_row, box_row + 3)
                for column in range(box_column, box_column + 3)
            ]
            if set(values) != set(range(1, 10)):
                return False
    return True


def find_empty_cell(board: Board) -> Optional[Position]:
    """Find the next empty cell, or None when the board has no empty cells."""
    for row in range(9):
        for column in range(9):
            if board[row][column] == 0:
                return row, column
    return None


def solve(board: Board) -> bool:
    """Solve a board in place using recursive backtracking."""
    empty_cell = find_empty_cell(board)
    if empty_cell is None:
        return is_valid_solution(board)

    row, column = empty_cell
    for number in range(1, 10):
        if is_valid_move(board, row, column, number):
            board[row][column] = number
            if solve(board):
                return True
            board[row][column] = 0
    return False


def create_puzzle(difficulty: str) -> Tuple[Board, Board]:
    """Choose a puzzle and remove extra clues for the selected difficulty."""
    difficulty = difficulty.lower()
    if difficulty not in DIFFICULTY_REMOVALS:
        raise ValueError("Difficulty must be easy, medium, or hard.")

    puzzle = copy_board(random.choice(PUZZLES))
    removals = DIFFICULTY_REMOVALS[difficulty]
    empty_cells = [
        (row, column)
        for row in range(9)
        for column in range(9)
        if puzzle[row][column] != 0
    ]
    for row, column in random.sample(empty_cells, min(removals, len(empty_cells))):
        puzzle[row][column] = 0

    # Verify the selected puzzle with the same solver used by the project.
    verification_board = copy_board(puzzle)
    if not solve(verification_board):
        raise ValueError("The selected puzzle could not be solved.")
    return puzzle, copy_board(SOLVED_BOARD)


def is_complete(board: Board, solution: Board) -> bool:
    """Check both that no cells are empty and that the solution is valid."""
    return find_empty_cell(board) is None and board == solution and is_valid_solution(board)


def give_hint(board: Board, solution: Board) -> Optional[Position]:
    """Fill one empty cell from the known solution and return its position."""
    empty_cell = find_empty_cell(board)
    if empty_cell is None:
        return None
    row, column = empty_cell
    board[row][column] = solution[row][column]
    return row, column
