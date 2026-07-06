"""
2-Player Tic-Tac-Toe
--------------------
Two players take turns entering a row and column (0-2) to place
their sign on a 3x3 board. Player 1 = 'X', Player 2 = 'O'.
The script checks after every move whether someone has won or
whether the board is full (a draw).
"""


def create_board():
    """Create and return an empty 3x3 board."""
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board):
    """Print the board in a readable grid format."""
    print()
    for i, row in enumerate(board):
        print(" " + " | ".join(row))
        if i < 2:
            print("---+---+---")
    print()


def get_move(player, board):
    """
    Ask the current player for a row and column.
    Keeps asking until the input is valid:
      - both values are integers between 0 and 2
      - the chosen square is currently empty
    Returns the validated (row, col) as integers.
    """
    while True:
        try:
            raw = input(f"Player {player}, enter your move as 'row col' (0-2 0-2): ")
            row_str, col_str = raw.split()
            row, col = int(row_str), int(col_str)
        except ValueError:
            print("Invalid input. Please enter two numbers, e.g. '1 2'.")
            continue

        if row not in (0, 1, 2) or col not in (0, 1, 2):
            print("Row and column must each be 0, 1, or 2. Try again.")
            continue

        if board[row][col] != " ":
            print("That square is already taken. Choose an empty square.")
            continue

        return row, col


def check_win(board, symbol):
    """Return True if 'symbol' (X or O) has three in a row anywhere."""
    # Rows
    for row in board:
        if all(cell == symbol for cell in row):
            return True

    # Columns
    for col in range(3):
        if all(board[row][col] == symbol for row in range(3)):
            return True

    # Diagonals
    if all(board[i][i] == symbol for i in range(3)):
        return True
    if all(board[i][2 - i] == symbol for i in range(3)):
        return True

    return False


def check_draw(board):
    """Return True if every square is filled (no blanks remain)."""
    return all(cell != " " for row in board for cell in row)


def play_game():
    """Main game loop."""
    board = create_board()
    current_symbol = "X"   # Player 1 starts with X
    player_number = 1
    game_over = False

    print("Welcome to 2-Player Tic-Tac-Toe!")

    while not game_over:
        print_board(board)
        row, col = get_move(player_number, board)
        board[row][col] = current_symbol

        if check_win(board, current_symbol):
            print_board(board)
            print(f"Player {player_number} ('{current_symbol}') wins! 🎉")
            game_over = True
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            game_over = True
        else:
            # Switch turns
            current_symbol = "O" if current_symbol == "X" else "X"
            player_number = 2 if player_number == 1 else 1


if __name__ == "__main__":
    play_game()