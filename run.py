import random
import time

#Global Variables
BOARD_SIZE = 10
NUMBER_SHIPS = 4
SHOTS_LEFT = 50
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BOARD = [["." for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
SHIP_LOCATIONS = [[]]
NUM_SHIPS_SUNK = 0
GAME_OVER = False

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

    ALPHABET = ALPHABET[:len(BOARD) + 1]

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
    """
    Function to attempt to place a ship on the board
    """
    global BOARD_SIZE

    row_start, row_end, col_start, col_end = row, row + 1, col, col + 1
    if direction == "left":
        if col - length < 0:
            return False
        col_start = col - length + 1
    elif direction == "down":
        if row + length >= BOARD_SIZE:
            return False
        row_end = row + length
    elif direction == "right":
        if col + length >= BOARD_SIZE:
            return False
        col_end = col + length
    elif direction == "up":
        if row - length < 0:
            return False
        row_start = row - length + 1

    return place_ship(row_start, row_end, col_start, col_end)

def place_ship(row_start, row_end, col_start, col_end):
    global BOARD, SHIP_LOCATIONS

    if any(BOARD[r][c] != "." for r in range(row_start, row_end) for c in range(col_start, col_end)):
        return False

    SHIP_LOCATIONS.append([row_start, row_end, col_start, col_end])

    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            BOARD[r][c] = "0"

    return True

def valid_bullet():
    """
    Function to determine whether the input from the user is valid
    """
    global ALPHABET, BOARD

    is_valid = False
    row = -1
    col = -1
    while not is_valid:
        place_bullet = input("Enter a row (A - J), and a column (0 - 9) such as B4: ")
        place_bullet = place_bullet.upper()
        if len(place_bullet) != 2:
            print("Placement Error: Please enter ONE row and ONE column such as B4")
            continue
        row = ALPHABET.find(place_bullet[0])
        col = int(place_bullet[1])
        if not (0 <= row < BOARD_SIZE) or not (0 <= col < BOARD_SIZE):
            print("Placement Error: Please enter letter (A - J) for row and number (0 - 9) for column such as B4")
            continue
        if BOARD[row][col] == "#" or BOARD[row][col] == "X":
            print("Shots already fired there, try another target!")
            continue
        if BOARD[row][col] == "." or BOARD[row][col] == "0":
            is_valid = True

    return row, col


def make_shot():
    """
    Function that allows the player to make a shot
    """
    global BOARD, NUM_SHIPS_SUNK, SHOTS_LEFT, GAME_OVER

    def ship_sunk(row, col):
        global SHIP_LOCATIONS
        global BOARD

        for location in SHIP_LOCATIONS:
            row_start, row_end, col_start, col_end = location
            if row_start <= row <= row_end and col_start <= col <= col_end:
                for r in range(row_start, row_end + 1):
                    for c in range(col_start, col_end + 1):
                        if BOARD[r][c] != "X":
                            return False
        return True

    if SHOTS_LEFT <= 0:
        print("You've run out of bullets, You lost the game!")
        print("Better luck next time!")
        GAME_OVER = True
        return

    row, col = valid_bullet()
    print("")
    print("--------------------")

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

 
def is_game_over():
    """
    function to check of the game is over
    and whether the player wins or looses
    """
    global NUM_SHIPS_SUNK, NUMBER_SHIPS, SHOTS_LEFT, GAME_OVER

    if NUMBER_SHIPS == NUM_SHIPS_SUNK:
        print("Congratulations, You Won!")
        GAME_OVER = True
    elif SHOTS_LEFT <= 0:
        print("Youve run out of bullets, You lost the game!")
        print("Better luck next time!")
        GAME_OVER = True

def main():
    """
    The main function
    determines what order the functions are run in
    controls the working of the game
    """
    global GAME_OVER

    print("     ----- WELCOME TO -----     ")
    print("""
BBBB      A   TTTTT TTTTT L     EEEEE  SSS  H   H IIIII PPPP   SSS  
B   B    A A    T     T   L     E     S   S H   H   I   P   P S   S
B  B    A   A   T     T   L     E     S     H   H   I   P   P S    
BBB     AAAAA   T     T   L     EEEEE  SSS  HHHHH   I   PPP    SSS  
B  B    A   A   T     T   L     E         S H   H   I   P         S
B   B   A   A   T     T   L     E     S   S H   H   I   P     S   S
BBBB    A   A   T     T   LLLLL EEEEE  SSS  H   H IIIII P      SSS         
""")
    print("--------------------")

    setup_game()
    print("You have 50 shots to destroy 4 Ships, Let the battle commence!\n")
    
    make_board()

    while GAME_OVER is False:
        print_board()
        print("\nNumber of Ships remaining: " + str(NUMBER_SHIPS - NUM_SHIPS_SUNK))
        print(f"You have {str(SHOTS_LEFT)} Shots remaining.\n")
        make_shot()
        print("--------------------\n")
        print("")
        is_game_over()

if __name__ == "__main__":
    main()
