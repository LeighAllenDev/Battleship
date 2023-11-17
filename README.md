# BattleShips
## Code Institute Learner Project 03

## Intro
Battleship is a classic naval strategy game. This project version is a text-based interpretation implemented in Python, where players attempt to sink a fleet of enemy ships before running out of available shots.

The player chooses the board size, then chooses how many ships they have to find. The computer then calculates and places the ships on the board and provides the user with a calculated amount of shots to make the game fair yet balanced. 

Legend:
1. "." Empty space or water
2. "#" Water thats been hit, a miss as the space isn't part of a ship
3. "X" Part of a ship has been hit
4. "0" Part of a ship, this isn't seen by the player. However, it can be accessed in debug mode and it will locate all the ships on the board.

# Table of Contents
1. [Introduction](#intro)
2. [How to Play](#how-to-play)
    * [Rules](#rules)
    * [Game Set Up](#game-set-up)
    * [Playing the Game](#playing-the-game)
    * [How to Win](#how-to-win)
3. [Features](#features)
4. [Planning Phase](#planning-phase)
    * [User Stories](#user-stories)
    * [Site Aims](#site-aims)
    * [How This Is Achieved](#how-this-is-achieved)
    * [Game Play Flow chart](#game-play-flow-chart)
5. [Data Model](#data-model)
    * [Overview of Functions](#overview-of-functions)
    * [Logic Flow](#logic-flow)
6. [Testing Phase](#testing-phase)
    * [Manual Testing](#manual-testing)
    * [Bugs and Fixes](#bugs-and-fixes)
    * [Post Development Testing](#post-development-testing)
7. [Technologies Used](#technologies-used)
8. [Deployment](#deployment)
9. [Credits](#credits)


## How to Play
### Rules
This is a 1 player game where the user plays against the computer to find all computer generated ships on the board before they run out of shots.
### Game Set Up
1. The user chooses the board size.
    * This can be between 5 and 20
    * The board will be a square grid based on the users input. (e.g 5x5)
2. The User Chooses the amount of ships they have to find.
    * The program calculates whether the amount of ships will fit on 20% of the board
    * if the number they pick is out of range the program will ask them to pick between specific numbers
3. The amount of shots is calculated
    * The program calculates the amount of shots the user has based on how big the board is and how many shots they have chosen.

### Playing the Game
* Once the player has customised the game to their liking they will be prompted to pick a space on the grid.
* Provided the user makes a valid move, the board will then show one of two options:
    * '#' - This indicates they have hit empty water, a message is also displayed to indicate that their shot missed.
    * 'X' - This indicates that part of a ship has been hit. There will also be a confirmation message which says either:
        * "Bullseye! A ship has been shot" if only part of a ship has been shot
        * "Bullseye! You sunk my battleship!" if the whole ship has now been hit
* At the end of the game the users is given the oportinity to play again. Should they choose to play again the board resets and allows them to change the size and the amount of ships again.

### How to Win
To win the game you have to hit all the ships before you run out of bullets. Messages display in the terminal whether you win or loose:


## Features
#### Customisable Board Size
The user is able to choose their own board size between a 5x5 and 20x20 grid to give a wide array of size options which makes every time you play the game feel unique.
#### Variable Number of Ships
The user is able to decide how challenging their game is by choosing how many ships there are. There are some background calculations to make sure the board isn't overcrowded and that all the ships will be able to fit on the board without hanging off the edges.
#### Dynamic Shot Calculation
The amount of shots that the user is given is automatically generated based on the amount of ships they have chosen and the size of the board.
#### Intuiative UI
The board is easily laid out and the shots are clearly displayed so the user knows whether they have hit or missed a ship. there are also text prompts after every shot to tell the user the outcome of their shot.

The game utilizes ascii art to signify whether the player wins or looses. Examples of this can be seen in the *How to Win* section above.
#### Play Again Option

## Planning Phase

### User Stories
During the market research stage of this project, potential users asked the following:
* A user would like the ability to change the size of the board to make it either easier or more of a challenge as they don't often see this in a terminal based game.
* Users wanted the ability to change the amount of ships they have to find as this will give them a customised experience and change the difficulty.
* Users want a dinamic experience and the ability to play again at the end of the game. They said a lot of terminal games do not give the option to play again or personalise each game.
### Site Aims
* The site aims to give the user the chance to play a customizable version of the classic battleships game on the browser window or a terminal with no other software required. 
* It aims to allow the user to play on a size board they choose and a difficulty level they can pick with no coding or programing experience.
### How This is Achieved
This is achieved in the following ways:
* Deploying the game using Heroku allows for a terminal experience within the browser window without the need to install software such as an IDE.
* Allowing the user to customize there experience with resizable boards and amount of ships, as well as being able to reset the board and number of ships for each game.
### Game Play Flow Chart

## Data Model

### Overview of Functions
The game is made up of 10 core functions which work together to make main game work. A brief overview of these functions is as follows:

* **Setup_Game** - This function takes input from the user to determine the grid size, amount of ships they want to find and based of their choices, calculates the amount of shots the user gets.
* **Make_board** - This function takes the results of the user input and runs the calculations to make the board as well as calculating the ship size and direction then asigns their locations.
* **Print_Board** - Once all the calculations have been made, the board is then printed to the terminal with this function.
* **Attempt_Ship_Placement** - This function calculates the placement of the ships based on their randomly generated size and attempts to place them on the board. These will be hidden from the user.
* **Valid_Bullet** - This function takes in the users input for making the shot, calculates whether the input is valid i.e a single letter followed by a 1 or 2 digit number depending on the size of the board. If the input doesn't meet the requirements an error message is displayed to the user.
* **Make_Shot** - 

### Logic Flow

## Testing Phase

### Manual Testing

### Bugs and Fixes

### Post Development Testing

## Technologies Used
This project is solely made in the popular programing languge Python3 and it has been built using Visual Studio Code and a GitHub repository. The project is deployed with Heroku.
## Deployment

## Credits
