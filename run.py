import random
import time

#Global Variables
BOARD_SIZE = 10
NUMBER_SHIPS = 4
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
"""

def setup_game():
    """
    Function to allow the user to set up the game
    """
    global BOARD_SIZE, NUMBER_SHIPS, SHOTS_LEFT, BOARD
    try:
        BOARD_SIZE = int(input("Enter board size (e.g., 10 for a 10x10 board): "))
        NUMBER_SHIPS = int(input("Enter the number of ships: "))
        SHOTS_LEFT = int(input("Enter the number of shots you have: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        setup_game()

    BOARD = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    make_board()

def print_board():
    """
    Prints the board to the terminal
    """
    global BOARD, ALPHABET

    debug_mode = False

    ALPHABET = ALPHABET[:len(BOARD)]

    for row in range(len(BOARD)):
        print(ALPHABET[row], end=") ")
        for col in range(len(BOARD[row])):
            if BOARD[row][col] == "0":
                print("0" if debug_mode else ".", end=" ")
            else:
                print(BOARD[row][col], end=" ")
        print("")

    print(" ", end=" ")
    for i in range(len(BOARD[0])):
        print(i, end=" ")
    print("")


def make_board():
    """
    Makes a 10x10 grid board and places down ships randomly.
    """
    global BOARD, BOARD_SIZE, NUMBER_SHIPS, SHIP_LOCATIONS
    
    random.seed(time.time())

    rows, cols = (BOARD_SIZE, BOARD_SIZE)

    BOARD = [["." for _ in range(cols)] for _ in range(rows)]

    number_ships_placed = 0
    SHIP_LOCATIONS = []

    while number_ships_placed != NUMBER_SHIPS:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)
        if attempt_ship_placement(random_row, random_col, direction, ship_size):
            number_ships_placed += 1


def attempt_ship_placement(row, col, direction, length):
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

    if row_start < 0 or row_end >= BOARD_SIZE or col_start < 0 or col_end >= BOARD_SIZE:
        return False

    return place_ship(row_start, row_end, col_start, col_end)


def place_ship(row_start, row_end, col_start, col_end):
    global BOARD, SHIP_LOCATIONS

    for r in range(max(0, row_start - 1), min(BOARD_SIZE, row_end + 2)):
        for c in range(max(0, col_start - 1), min(BOARD_SIZE, col_end + 2)):
            if BOARD[r][c] != ".":
                return False

    SHIP_LOCATIONS.append([row_start, row_end, col_start, col_end])
    for r in range(row_start, row_end + 1):
        for c in range(col_start, col_end + 1):
            BOARD[r][c] = "0"

    return True


def valid_bullet():
    global ALPHABET, BOARD

    max_row_letter = ALPHABET[BOARD_SIZE - 1]
    max_col_number = BOARD_SIZE - 1

    is_valid = False
    while not is_valid:
        place_bullet = input(f"Enter a row (A - {max_row_letter}), and a column (0 - {max_col_number}) such as B4: ").upper()
        if (len(place_bullet) < 2 or len(place_bullet) > 3) or \
           (len(place_bullet) == 3 and BOARD_SIZE <= 10):
            print(f"Invalid input length. Please enter a letter (A - {max_row_letter}) for row and number (0 - {max_col_number}) for column.")
            continue
        if not place_bullet[0].isalpha() or place_bullet[0] > max_row_letter:
            print(f"Invalid row letter. Please enter a letter (A - {max_row_letter}) for row.")
            continue
        if not place_bullet[1:].isdigit() or int(place_bullet[1:]) > max_col_number:
            print(f"Invalid column number. Please enter a number (0 - {max_col_number}) for column.")
            continue

        row = ALPHABET.find(place_bullet[0])
        col = int(place_bullet[1:])
        is_valid = True

    return row, col



def make_shot():
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
    global SHIP_LOCATIONS, BOARD

    for location in SHIP_LOCATIONS:
        row_start, row_end, col_start, col_end = location
        if row_start <= row <= row_end and col_start <= col <= col_end:
            for r in range(row_start, row_end + 1):
                for c in range(col_start, col_end + 1):
                    if BOARD[r][c] != "X":
                        return False
    return True

 
def is_game_over():
    """
    function to check of the game is over
    and whether the player wins or looses
    """
    global NUM_SHIPS_SUNK, NUMBER_SHIPS, SHOTS_LEFT, GAME_OVER, GAME_TITLE

    if NUMBER_SHIPS == NUM_SHIPS_SUNK:
        print("Congratulations, You Won!\n")
        print("     ----- Thank You for playing -----     ")
        print(GAME_TITLE)
        print("--------------------")
        GAME_OVER = True
    elif SHOTS_LEFT <= 0:
        print("Youve run out of bullets, You lost the game!")
        print("Better luck next time!")
        print("     ----- Thank You for playing -----     ")
        print(GAME_TITLE)
        print("--------------------")
        GAME_OVER = True


def main():
    print("     ----- WELCOME TO -----     ")
    print(GAME_TITLE)  
    print("--------------------")
    setup_game()
    print(f"You have {SHOTS_LEFT} shots to destroy {NUMBER_SHIPS} Ships, Let the battle commence!\n")
    
    while not GAME_OVER:
        print_board()
        print("\nNumber of Ships remaining: " + str(NUMBER_SHIPS - NUM_SHIPS_SUNK))
        print(f"You have {SHOTS_LEFT} Shots remaining.\n")
        make_shot()
        print("--------------------\n")
        print("")
        is_game_over()

if __name__ == "__main__":
    main()

