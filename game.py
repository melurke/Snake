# Import packages
import random
from time import sleep as wait
from termcolor import colored
import os
import keyboard

def ClearScreen(): # Clear the screen so the game field is only shown once at a time
    os.system('cls' if os.name == 'nt' else 'clear')

def ChooseApplePosition(snakePos): # Choose a new position for the apple after it is eaten
    pos = [random.randint(1, 16), random.randint(1, 16)]
    while pos in snakePos:
        pos = [random.randint(1, 16), random.randint(1, 16)]
    return pos

def EatApple(headPos, snakePos, applePos, length): # Lengthen the snake if the apple is eaten and choose a new position for it
    if headPos == applePos:
        length += 1
        applePos = ChooseApplePosition(snakePos)
    else:
        snakePos.remove(snakePos[0])
    return applePos, length

def UpdateBoard(headPos, applePos, snakePos, board): # Update all the fields on the board
    for y in range(1, 17):
        for x in range(1, 17):
            pos = [x, y]
            if pos == applePos:   content = "*"
            elif pos == headPos:  content = "#"
            elif pos in snakePos: content = "+"
            else:                 content = "O"
            board.append(content)

def PrintBoard(board, length): # Clear the terminal and print the new board
    boardStr = ""
    for i, content in enumerate(board):
        if i % 16 == 0:
            boardStr += "\n"
        if content == "*":
            boardStr += "  " + colored(content, "red")
        elif content != "O":
            boardStr += "  " + colored(content, "green")
        else:
            boardStr += "  " + content
    ClearScreen()
    print(boardStr)
    print(f"\nScore: {length-2}")

def CheckInput(direction): # Wait for ~0.5 seconds and continuously check for player input
    for i in range(50):
        wait(0.01)
        if keyboard.is_pressed('w') and direction != [0, 1]:
            return [0, -1]
        if keyboard.is_pressed('a') and direction != [1, 0]:
            return [-1, 0]
        if keyboard.is_pressed('s') and direction != [0, -1]:
            return [0, 1]
        if keyboard.is_pressed('d') and direction != [-1, 0]:
            return [1, 0]
    return direction

def CheckDeath(headPos, snakePos): # Check if the snake is outside of the board or intersecting itself
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True

    isOffScreen = not (0 < headPos[0] < 17) or not (0 < headPos[1] < 17)
    if isOffScreen:
        return True
    return False

def Main():
    length = 1
    applePos = [10, 9]
    headPos = [9, 9]
    snakePos = [headPos.copy()]
    direction = [1, 0]

    while True:
        board = []
        # Update the position of the snake
        headPos[0] += direction[0]
        headPos[1] += direction[1]
        snakePos.append(headPos.copy())
        applePos, length = EatApple(headPos, snakePos, applePos, length) # Update length and apple position

        if CheckDeath(headPos, snakePos): # Check for death and end the game if neccessary
            break
        UpdateBoard(headPos, applePos, snakePos, board) # Update the board with all the new fields
        PrintBoard(board, length) # Print the board to the terminal
        wait(0.5) # Wait for half a second so the player can't spam inputs
        direction = CheckInput(direction) # Check for player input and update the direction
    print(f"\nYou lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function