# Write your code to expect a terminal of 80 characters wide and 24 rows high
"""
---- TO DO ---
choose the ships

place the ships on the board

make the board

make a function to make the shots

try to make it multi player (play against the computer)

make functions for hit or missing the ships

make the working game function
"""

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
    """
    Prints the board to the terminal
    """
    global BOARD
    global ALPHABET

    debug_mode = True

    alphabet = ALPHABET[0: len(BOARD) + 1]

    for row in range(len(BOARD)):
        print(ALPHABET[row], end=") ")
        for col in range(len(BOARD[row])):
            if BOARD[row][col] == "0":
                if debug_mode:
                    print("0", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(BOARD[row][col], end=" ")
        print("")

    print("  ", end=" ")
    for i in range(len(BOARD[0])):
        print(str(i), end=" ")
    print("")

def make_board():
    """
    makes a 10x10 grid board and places down ships randomly.
    """
    global BOARD
    global BOARD_SIZE
    global NUMBER_SHIPS
    global SHIP_LOCATIONS

    random.seed(time.time())

    rows, cols = (BOARD_SIZE, BOARD_SIZE)

    board = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
    
    number_ships_placed = 0

    SHIP_LOCATIONS = []

    while number_ships_placed != NUMBER_SHIPS:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(2,3,3,5)
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
    """
    Function to place ships on the board
    """
    global BOARD
    global SHIP_LOCATIONS

    all_valid = True
    for r in range(row_start, row_end):
        for c in range(col_start,col_end):
            if BOARD[r][c] != ".":
                all_valid = False
                break
    if all_valid:
        SHIP_LOCATIONS.append([row_start, row_end, col_start, col_end])
        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                BOARD[r][c] = "0"
    return all_valid

def valid_bullet():
    """
    function to get a valif row and column to place bullet
    """
    global ALPHABET
    global BOARD

    is_valid = False
    row = -1
    col = -1
    while is_valid is False:
        place_bullet = input("Enter a row (A - J), and a column (0 - 9) such as B4: ")
        place_bullet = place_bullet.upper()
        if len(place_bullet) <= 0 or len(place_bullet) > 2:
            print("Placement Error: Please enter ONE row and column such as B4")
            continue
        row = place_bullet[0]
        col = place_bullet[1]
        if not row.isalpha() or not col.isnumeric():
            print("Placement Error: Please enter letter (A - J) for row and number (0 - 9) for column such as B4")
            continue
        row = ALPHABET.find(row)
        if not (-1 < row < BOARD_SIZE):
            print("Placement Error: Please enter letter (A - J) for row and number (0 - 9) for column such as B4")
            continue
        col = int(col)
        if not (-1 < col < BOARD_SIZE):
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

    def ship_sunk():