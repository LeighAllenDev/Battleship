import random
import time

#Global Variables
BOARD = [[]]
BOARD_SIZE = 10
NUMBER_SHIPS = 4
SHIP_LOCATIONS = [[]]
SHOTS_LEFT = 50
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM_SHIPS_SUNK = 0
GAME_OVER = False


def print_board():
    global BOARD
    global ALPHABET

    debug_mode = False

    alphabet = ALPHABET[0: len(BOARD) + 1]

    for row in range(len(BOARD)):
        print(ALPHABET[row], end=") ")
        for col in range(len(BOARD[row])):
            if BOARD[row][col] == "#" or BOARD[row][col] == "X":
                print(BOARD[row][col], end=" ")
            elif BOARD[row][col] == "0" and debug_mode:
                print("0", end=" ")
            else:
                print(".", end=" ")
        print("")

    print("  ", end=" ")
    for i in range(len(BOARD[0])):
        print(str(i), end=" ")
    print("")


def make_board():
    global BOARD
    global BOARD_SIZE
    global NUMBER_SHIPS
    global SHIP_LOCATIONS

    random.seed(time.time())

    rows, cols = (BOARD_SIZE, BOARD_SIZE)

    
    BOARD = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
        BOARD.append(row)

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
    global BOARD
    global SHIP_LOCATIONS

    all_valid = True
    for r in range(row_start, row_end):
        for c in range(col_start, col_end):
            if BOARD[r][c] != ".":
                all_valid = False
                break

        if not all_valid:
            break

    if all_valid:
        SHIP_LOCATIONS.append([row_start, row_end, col_start, col_end])
        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                BOARD[r][c] = "0"

    return all_valid



def valid_bullet():
    global ALPHABET
    global BOARD

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
    global BOARD
    global NUM_SHIPS_SUNK
    global SHOTS_LEFT
    global GAME_OVER

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
    global NUM_SHIPS_SUNK
    global NUMBER_SHIPS
    global SHOTS_LEFT
    global GAME_OVER

    if NUMBER_SHIPS == NUM_SHIPS_SUNK:
        print("Congratulations, You Won!")
        GAME_OVER = True
    elif SHOTS_LEFT <= 0:
        print("Youve run out of bullets, You lost the game!")
        print("Better luck next time!")
        GAME_OVER = True

def main():
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
    print("You have 50 shots to destroy 4 Ships, Let the battle commence!")
    
    make_board()

    while GAME_OVER is False:
        print_board()
        print("Number of Ships remaining: " + str(NUMBER_SHIPS - NUM_SHIPS_SUNK))
        print(f"You have {str(SHOTS_LEFT)} Shots remaining.")
        make_shot()
        print("--------------------")
        print("")
        is_game_over()

if __name__ == "__main__":
    main()
