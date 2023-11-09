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

