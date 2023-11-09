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
# Global variable for the game board
board = [[]]
# Global variable for the game board size
board_size = 10

# Number of ships Global variable
number_ships = 4

# global variable for ship locations
ship_locations = [[]]

# Global variable for shots remaining
shots_left = 50

# Variable for Global alphabet
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def print_board():
    """
    Prints the board to the terminal
    """
    global board
    global alphabet

    debug_mode = True

    alphabet = alphabet[0: len(board) + 1]

    for row in range(len(board)):
        print(alphabet[row], end=") ")
        for col in range(len(board[row])):
            if board[row][col] == "0":
                if debug_mode:
                    print("0", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(board[row][col], end=" ")
        print("")

    print("  ", end=" ")
    for i in range(len(board[0])):
        print(str(i), end=" ")
    print("")

def make_board():
    """
    makes a 10x10 grid board and places down ships randomly.
    """
    global board
    global board_size
    global number_ships
    global ship_locations

    random.seed(time.time())

    rows, cols = (board_size, board_size)

    board = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
    
    number_ships_placed = 0

    ship_locations = []

    while number_ships_placed != number_ships:
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
    global board_size

    row_start, row_end, col_start, col_end = row, row + 1, col, col + 1
    if direction == "left":
        if col - length < 0:
            return False
        col_start = col - length + 1
    elif direction == "down":
        if row + length >= board_size:
            return False
        row_end = row + length
    elif direction == "right":
        if col + length >= board_size:
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
    global board
    global ship_locations

    all_valid = True
    for r in range(row_start, row_end):
        for c in range(col_start,col_end):
            if board[r][c] != ".":
                all_valid = False
                break
    if all_valid:
        ship_locations.append([row_start, row_end, col_start, col_end])
        for r in range(row_start, row_end):
            for c in range(col_start, col_end):
                board[r][c] = "0"
    return all_valid

def valid_bullet():
    """
    function to get a valif row and column to place bullet
    """
    global alphabet
    global board

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
        row = alphabet.find(row)
        if not (-1 < row < board_size):
            print("Placement Error: Please enter letter (A - J) for row and number (0 - 9) for column such as B4")
            continue
        col = int(col)
        if not (-1 < col < board_size):
            print("Placement Error: Please enter letter (A - J) for row and number (0 - 9) for column such as B4")
            continue
        if board[row][col] == "#" or board[row][col] == "X":
            print("Shots already fired there, try another target!")
            continue
        if board[row][col] == "." or board[row][col] == "0":
            is_valid = True

    return row, col 
