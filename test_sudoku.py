"""Beginner-friendly tests for the Sudoku rules and solver."""

import unittest

from sudoku import (
    SOLVED_BOARD,
    copy_board,
    find_empty_cell,
    is_fixed_cell,
    is_complete,
    is_valid_move,
    is_valid_solution,
    solve,
)


class SudokuTests(unittest.TestCase):
    def setUp(self):
        self.board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]

    def test_valid_move(self):
        self.assertTrue(is_valid_move(self.board, 0, 2, 4))

    def test_invalid_row_move(self):
        self.assertFalse(is_valid_move(self.board, 0, 2, 5))

    def test_invalid_column_move(self):
        self.assertFalse(is_valid_move(self.board, 0, 2, 8))

    def test_invalid_box_move(self):
        self.assertFalse(is_valid_move(self.board, 0, 2, 9))

    def test_fixed_cell_protection_is_checked_by_original_board(self):
        self.assertTrue(is_fixed_cell(self.board, 0, 0))
        self.assertFalse(is_fixed_cell(self.board, 0, 2))

    def test_completed_valid_board(self):
        board = copy_board(SOLVED_BOARD)
        self.assertTrue(is_complete(board, SOLVED_BOARD))
        self.assertTrue(is_valid_solution(board))

    def test_invalid_completed_board(self):
        board = copy_board(SOLVED_BOARD)
        board[0][0] = 6
        self.assertFalse(is_complete(board, SOLVED_BOARD))
        self.assertFalse(is_valid_solution(board))

    def test_solver_fills_board(self):
        board = copy_board(self.board)
        self.assertTrue(solve(board))
        self.assertEqual(board, SOLVED_BOARD)
        self.assertIsNone(find_empty_cell(board))


if __name__ == "__main__":
    unittest.main()
