# Sudoku Game

A beginner-friendly Sudoku game played in the terminal. The player chooses a difficulty, enters numbers into empty cells, can request limited hints, and wins by completing a valid Sudoku board.

## Features

- 9x9 board with visible 3x3 boxes
- Easy, Medium, and Hard difficulty levels
- Two starter puzzle patterns selected randomly
- Protected original clues
- Input validation and clear error messages
- Backtracking solver and full-solution validation
- Up to three hints per game
- Score and mistake tracking
- Main menu with instructions and replay support
- Standard-library-only Python code

## How It Works

The game keeps two boards: the original puzzle, which identifies fixed clues, and the player's current board. A separate solved board supplies the correct answer for the selected puzzle. Every move is checked against row, column, and 3x3 box rules. The game only reports a win when the board is full and matches a valid solution.

## Technology

- Python 3
- Python standard library (`random`, `copy`, `typing`, and `unittest`)
- No external packages are required

## Run the Game

Open this folder in VS Code and run:

```text
python main.py
```

On Windows, `py main.py` also works. Start the program from VS Code by opening `main.py` and selecting **Run Python File**.

## Controls

- `1`, `2`, or `3` in the main menu: new game, instructions, or quit
- Choose `1`, `2`, or `3` for Easy, Medium, or Hard
- Enter moves as `row column number`, for example `3 5 7`
- Enter `h` for a hint
- Enter `0 0 0` or `q` to leave a game

Rows and columns are numbered from 1 to 9. A dot (`.`) means an empty cell.

## Difficulty

- **Easy:** a randomly selected starting pattern
- **Medium:** the selected pattern with 8 additional clues removed
- **Hard:** the selected pattern with 18 additional clues removed

All puzzles use a known valid completed board, so every generated board is solvable by that answer. The solver in `sudoku.py` can also solve a puzzle from scratch.

## Scoring

- Start: 100 points
- Correct move: +2 points
- Wrong move: -5 points and one mistake
- Hint: -10 points
- Score never falls below zero

## Project Structure

```text
Suduko/
├── main.py          # Menu, display, input, scoring, and game flow
├── sudoku.py        # Board rules, puzzles, hints, and solver
├── test_sudoku.py   # Tests for important Sudoku behavior
├── README.md        # Project documentation
└── requirements.txt # Explains that no packages are needed
```

## Example Gameplay

```text
Difficulty: Medium
Score: 100 | Mistakes: 0 | Hints remaining: 3

    1 2 3   4 5 6   7 8 9
  +-------+-------+-------+
1 | 5 . . | 6 . . | 9 . . |
...
Enter row column number, h for a hint, or q to quit: 1 2 3
Number placed successfully!
```

## Tests

Run the tests with:

```text
python -m unittest test_sudoku.py -v
```

The tests cover valid moves, row/column/box conflicts, clue protection, valid and invalid completed boards, and the backtracking solver.

## Future Improvements

- Generate randomized Sudoku solutions instead of using a small puzzle collection
- Guarantee uniqueness when removing clues
- Add a timer and a high-score table
- Add a graphical interface using a separate project layer
