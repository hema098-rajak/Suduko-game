"""Terminal user interface for the Sudoku game."""

from typing import Optional, Tuple

from sudoku import (
    Board,
    create_puzzle,
    give_hint,
    is_fixed_cell,
    is_complete,
    is_valid_move,
)


def display_board(board: Board) -> None:
    """Print a readable 9x9 board with visible 3x3 boxes."""
    print("\n    1 2 3   4 5 6   7 8 9")
    print("  +-------+-------+-------+")
    for row_number, row in enumerate(board, start=1):
        values = [str(value) if value else "." for value in row]
        print(f"{row_number} | {' '.join(values[0:3])} | {' '.join(values[3:6])} | {' '.join(values[6:9])} |")
        if row_number in (3, 6, 9):
            print("  +-------+-------+-------+")


def choose_difficulty() -> Optional[str]:
    """Ask for a difficulty and return it, or None to return to the menu."""
    choices = {"1": "easy", "2": "medium", "3": "hard"}
    while True:
        print("\nChoose difficulty:")
        print("1. Easy   (more clues)")
        print("2. Medium (fewer clues)")
        print("3. Hard   (fewest clues)")
        print("0. Back to menu")
        choice = input("Enter your choice: ").strip().lower()
        if choice == "0":
            return None
        if choice in choices:
            return choices[choice]
        print("Please enter 1, 2, 3, or 0.")


def read_move() -> Optional[Tuple[int, int, int]]:
    """Read a move, returning None for quit or hint commands."""
    command = input("\nEnter row column number, h for a hint, or q to quit: ").strip().lower()
    if command in ("q", "quit", "0 0 0"):
        return None
    if command in ("h", "hint"):
        return (-1, -1, -1)

    parts = command.split()
    if len(parts) != 3:
        print("Enter exactly three numbers, for example: 3 5 7")
        return (-2, -2, -2)
    try:
        row, column, number = (int(part) for part in parts)
    except ValueError:
        print("Rows, columns, and numbers must be numeric.")
        return (-2, -2, -2)
    return row, column, number


def play_game(difficulty: str) -> None:
    """Run one complete game of the selected difficulty."""
    original_board, solution = create_puzzle(difficulty)
    board = [row[:] for row in original_board]
    score = 100
    mistakes = 0
    hints_remaining = 3

    while True:
        print("\n=================================")
        print("          SUDOKU GAME")
        print("=================================")
        print(f"Difficulty: {difficulty.title()}")
        print(f"Score: {score} | Mistakes: {mistakes} | Hints remaining: {hints_remaining}")
        display_board(board)

        if is_complete(board, solution):
            print("Congratulations! You solved the Sudoku puzzle!")
            input("Press Enter to return to the menu.")
            return

        move = read_move()
        if move is None:
            print("Game ended. Returning to the main menu.")
            return
        if move == (-1, -1, -1):
            if hints_remaining == 0:
                print("You have no hints remaining.")
                continue
            hinted_cell = give_hint(board, solution)
            if hinted_cell is None:
                continue
            hints_remaining -= 1
            score = max(0, score - 10)
            row, column = hinted_cell
            print(f"Hint filled row {row + 1}, column {column + 1}.")
            continue
        if move == (-2, -2, -2):
            continue

        row, column, number = move
        if not (1 <= row <= 9 and 1 <= column <= 9):
            print("Invalid row or column. Use numbers from 1 to 9.")
            continue
        if not 1 <= number <= 9:
            print("Invalid number. Use a number from 1 to 9.")
            continue

        row_index, column_index = row - 1, column - 1
        if is_fixed_cell(original_board, row_index, column_index):
            print("You cannot change this cell.")
            continue
        if board[row_index][column_index] == number:
            print("That number is already in the cell.")
            continue
        if number != solution[row_index][column_index] or not is_valid_move(board, row_index, column_index, number):
            mistakes += 1
            score = max(0, score - 5)
            print("Invalid move! The number conflicts with the Sudoku rules.")
            continue

        board[row_index][column_index] = number
        score += 2
        print("Number placed successfully!")


def show_instructions() -> None:
    """Print the controls and rules for a new player."""
    print("\nINSTRUCTIONS")
    print("Fill every empty cell so each row, column, and 3x3 box contains 1 through 9.")
    print("Enter a move as: row column number (example: 3 5 7).")
    print("Enter h for a hint, or 0 0 0 / q to leave the current game.")
    print("Given numbers cannot be changed. You may use up to 3 hints per game.")
    input("\nPress Enter to return to the menu.")


def main() -> None:
    """Show the main menu until the player chooses to quit."""
    while True:
        print("\n===== SUDOKU GAME =====")
        print("1. New Game")
        print("2. Instructions")
        print("3. Quit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            difficulty = choose_difficulty()
            if difficulty is not None:
                play_game(difficulty)
        elif choice == "2":
            show_instructions()
        elif choice == "3":
            print("Thanks for playing Sudoku!")
            break
        else:
            print("Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
