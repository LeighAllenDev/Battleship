import random
import time
import re

# Global Variables
BOARD_SIZE = 10
MAX_BOARD_SIZE = 20
NUMBER_SHIPS = 4
MAX_SHIPS = 10
MAX_SHIPS_ALLOWED = 2
SHOTS_LEFT = 50
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BOARD = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
SHIP_LOCATIONS = []
NUM_SHIPS_SUNK = 0
GAME_OVER = False
GAME_TITLE = """
BBBB      A   TTTTT TTTTT L     EEEEE  SSS  H   H IIIII PPPP   SSS
B   B    A A    T     T   L     E     S   S H   H   I   P   P S   S
B  B    A   A   T     T   L     E     S     H   H   I   P   P S
BBB     AAAAA   T     T   L     EEEEE  SSS  HHHHH   I   PPP    SSS
B  B    A   A   T     T   L     E         S H   H   I   P         S
B   B   A   A   T     T   L     E     S   S H   H   I   P     S   S
BBBB    A   A   T     T   LLLLL EEEEE  SSS  H   H IIIII P      SSS
\n"""
WIN = """
__  __               _       ___       __
\ \/ /___  __  __   | |     / (_)___  / /
 \  / __ \/ / / /   | | /| / / / __ \/ /
 / / /_/ / /_/ /    | |/ |/ / / / / /_/
/_/\____/\__,_/     |__/|__/_/_/ /_(_)
\n"""
LOOSE = """
 __  __            __
 \ \/ /__  __ __  / /  ___  ___  ___ ___
  \  / _ \/ // / / /__/ _ \/ _ \(_-</ -_) _ _
  /_/\___/\_,_/ /____/\___/\___/___/\__(_|_|_)
\n"""


def setup_game():
    """
    Function to set up the game perameters
    """
    global BOARD_SIZE, NUMBER_SHIPS, SHOTS_LEFT, BOARD

    while True:
        try:
            BOARD_SIZE = int(input("""Enter board size
(e.g., 10 for a 10x10 board): """))
            if not 5 <= BOARD_SIZE <= MAX_BOARD_SIZE:
                print(f"""Invalid board size.
                Please enter a size between 5 and {MAX_BOARD_SIZE}.""")
                continue

            max_ships_allowed = (BOARD_SIZE * BOARD_SIZE) // 5

            NUMBER_SHIPS = int(input("Enter the number of ships: "))
            if not 1 <= NUMBER_SHIPS <= max_ships_allowed:
                print(f"""Invalid number of ships.
                Please enter a number between 1 and {max_ships_allowed}.""")
                continue

            base_shots = int(BOARD_SIZE**2 * 0.2)
            extra_shots_per_ship = 3
            SHOTS_LEFT = base_shots + (NUMBER_SHIPS * extra_shots_per_ship)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    BOARD = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def print_board():
    """
    Function that prints the board to the terminal
    """
    global BOARD, ALPHABET

    debug_mode = False

    displayed_alphabet = ALPHABET[:BOARD_SIZE]

    print("   ", end="")
    for i in range(1, BOARD_SIZE + 1):
        print(f"{i: >2}", end=" ")
    print()

    for row in range(BOARD_SIZE):
        print(f"{displayed_alphabet[row]: <2}) ", end="")
        for col in range(BOARD_SIZE):
            if BOARD[row][col] == "0":
                print("0" if debug_mode else ".", end="  ")
            else:
                print(BOARD[row][col], end="  ")
        print()


def make_board():
    """
    Function to make the board
    """
    global BOARD, BOARD_SIZE, NUMBER_SHIPS, SHIP_LOCATIONS
    random.seed(time.time())

    rows, cols = (BOARD_SIZE, BOARD_SIZE)
    BOARD = [["." for _ in range(cols)] for _ in range(rows)]
    SHIP_LOCATIONS = []

    number_ships_placed = 0
    attempts = 0

    while number_ships_placed < NUMBER_SHIPS:
        if attempts > 10:
            BOARD = [["." for _ in range(cols)] for _ in range(rows)]
            SHIP_LOCATIONS = []
            number_ships_placed = 0
            attempts = 0

        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(2, min(6, BOARD_SIZE // 2))

        if attempt_ship_placement(
                random_row, random_col, direction, ship_size):
            number_ships_placed += 1

        attempts += 1


def attempt_ship_placement(row, col, direction, length):
    """
    Function to calculate ship placement
    """
    global BOARD_SIZE

    row_start, row_end, col_start, col_end = row, row, col, col

    if direction == "left":
        if col - length < 0:
            return False
        col_start = col - length + 1
    elif direction == "right":
        if col + length > BOARD_SIZE:
            return False
        col_end = col + length - 1
    elif direction == "up":
        if row - length < 0:
            return False
        row_start = row - length + 1
    elif direction == "down":
        if row + length > BOARD_SIZE:
            return False
        row_end = row + length - 1

    if (row_start < 0 or row_end >= BOARD_SIZE
        or col_start < 0 or col_end >= BOARD_SIZE):
        return False

    return place_ship(row_start, row_end, col_start, col_end)


def place_ship(row_start, row_end, col_start, col_end):
    """
    Function to place a ship on the board
    """
    global BOARD, SHIP_LOCATIONS

    for r in range(row_start, row_end + 1):
        for c in range(col_start, col_end + 1):
            if BOARD[r][c] != ".":
                return False

    SHIP_LOCATIONS.append([row_start, row_end, col_start, col_end])
    for r in range(row_start, row_end + 1):
        for c in range(col_start, col_end + 1):
            BOARD[r][c] = "0"

    return True


def valid_bullet():
    """
    Function that determines whether shots are valid
    """
    global ALPHABET, BOARD

    max_row_letter = ALPHABET[BOARD_SIZE - 1]
    max_col_number = BOARD_SIZE

    is_valid = False
    while not is_valid:
        place_bullet = input(f"""Enter a row (A - {max_row_letter}),
And a column (1 - {max_col_number}) such as B1: """).upper()

        pattern = f"""^[A-{max_row_letter}](?:[1-9]|1
        [0-9]|2[0-{BOARD_SIZE % 10}])$"""
        if not re.match(pattern, place_bullet):
            print(f"""Invalid input. Please enter a letter
            (A - {max_row_letter}) for row and number
            (1 - {max_col_number}) for column.""")
            continue

        row = ALPHABET.find(place_bullet[0])
        col = int(place_bullet[1:]) - 1

        if not (0 <= row < BOARD_SIZE) or not (0 <= col < BOARD_SIZE):
            print(f"""Invalid coordinates.
Please enter a valid row and column within the board range.""")
            continue

        is_valid = True

    return row, col


def make_shot():
    """
    Function to make a shot
    """
    global BOARD, NUM_SHIPS_SUNK, SHOTS_LEFT

    row, col = valid_bullet()
    print("\n--------------------")

    if BOARD[row][col] == ".":
        print("You missed, No ships were hit")
        BOARD[row][col] = "#"
    elif BOARD[row][col] == "0":
        print("Bullseye!", end=" ")
        BOARD[row][col] = "X"
        if ship_sunk(row, col):
            print("You sunk my battleship!")
            NUM_SHIPS_SUNK += 1
        else:
            print("A ship has been shot")

    SHOTS_LEFT -= 1


def ship_sunk(row, col):
    """
    Function to determine whether ships are sunk
    """
    global SHIP_LOCATIONS, BOARD

    for location in SHIP_LOCATIONS:
        row_start, row_end, col_start, col_end = location
        if row_start <= row <= row_end and col_start <= col <= col_end:
            for r in range(row_start, row_end + 1):
                for c in range(col_start, col_end + 1):
                    if BOARD[r][c] != "X":
                        return False
    return True


def reveal_ships():
    """
    Reveals ships at the end of the game
    """
    global BOARD, SHIP_LOCATIONS

    for ship in SHIP_LOCATIONS:
        row_start, row_end, col_start, col_end = ship
        for r in range(row_start, row_end + 1):
            for c in range(col_start, col_end + 1):
                if BOARD[r][c] == "0":
                    BOARD[r][c] = "S"


def is_game_over():
    """
    function to check of the game is over
    and whether the player wins or looses
    """
    global NUM_SHIPS_SUNK, NUMBER_SHIPS, SHOTS_LEFT
    global GAME_OVER, GAME_TITLE, WIN, LOOSE

    if NUMBER_SHIPS == NUM_SHIPS_SUNK:
        print(WIN)

        GAME_OVER = True
    elif SHOTS_LEFT <= 0:
        print("Youve run out of bullets")
        print("--------------------")
        print(LOOSE)
        print("--------------------")
        print("Better luck next time!")
        reveal_ships()
        print_board()
        print("--------------------")
        GAME_OVER = True


def main():
    """
    Function to control the order the functions run in the game
    """
    print("---------- WELCOME TO BATTLESHIPS ----------")
    print(GAME_TITLE)
    print("--------------------")

    play_again = True
    while play_again:
        global NUM_SHIPS_SUNK, SHIP_LOCATIONS, BOARD, GAME_OVER

        NUM_SHIPS_SUNK = 0
        SHIP_LOCATIONS = []
        BOARD = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        GAME_OVER = False

        setup_game()
        make_board()
        print(f"""You have {SHOTS_LEFT} shots to destroy {NUMBER_SHIPS} Ships,
Let the battle commence!\n""")

        while not GAME_OVER:
            print_board()
            print("")
            print(f"Number of Ships remaining: {NUMBER_SHIPS - NUM_SHIPS_SUNK}")
            print(f"You have {SHOTS_LEFT} Shots remaining.\n")
            make_shot()
            print("--------------------")
            print("")
            is_game_over()

        while True:
            response = input("""Do you want to play again?
(yes/no): """).lower().strip()
            if response in ["yes", "y"]:
                play_again = True
                break
            elif response in ["no", "n"]:
                play_again = False
                print("\n     ----- Thank You for playing -----     ")
                print(GAME_TITLE)
                print("--------------------")
                break
            else:
                print("Invalid response. Please enter 'yes' or 'no'.")


if __name__ == "__main__":
    main()