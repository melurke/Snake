# Import packages
from lib2to3.pytree import NegatedPattern
import random
from time import sleep as wait
from termcolor import colored
import os

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

def ValidNeighbor(pos):
    if not (0 < pos[0] < 17):
        return False
    if not (0 < pos[1] < 17):
        return False
    return True

def GenerateNeighbors(pos):
    possibleNeighbors = [[pos[0], pos[1] + 1], [pos[0], pos[1] - 1], [pos[0] + 1, pos[1]], [pos[0] - 1, pos[1]]]
    neighborList = []
    for neighbor in possibleNeighbors:
        if ValidNeighbor(neighbor):
            neighborList.append(neighbor)
    return neighborList

def GenerateDijkstraValues(applePos, snakePos):
    values = [128] * 256
    for pos in snakePos:
        values[(pos[0] + 16 * (pos[1] - 1)) - 1] = 129
    fields = [applePos]
    values[applePos[0] + 16 * applePos[1] - 17] = 0
    while fields != []:
        for pos in fields.copy():
            neighbors = GenerateNeighbors(pos)
            for neighbor in neighbors:
                if values[neighbor[0] + 16 * (neighbor[1] - 1) - 1] == 128:
                    values[neighbor[0] + 16 * (neighbor[1] - 1) - 1] = values[pos[0] + 16 * (pos[1] - 1) - 1] + 1
                    fields.append(neighbor)
            fields.remove(pos)
        oldFields = fields.copy()
        fields = []
        for field in oldFields:
            if not field in fields:
                fields.append(field)
    values[applePos[0] + 16 * (applePos[1] - 1) - 1] = 0
    return values

def UpdateBoard(headPos, applePos, snakePos, board): # Update all the fields on the board
    values = GenerateDijkstraValues(applePos, snakePos)
    for y in range(1, 17):
        for x in range(1, 17):
            pos = [x, y]
            if pos == applePos:   content = "0"
            elif pos == headPos:  content = "#"
            elif pos in snakePos: content = "+"
            else:                 content = str(values[x + 16 * (y - 1) - 1])
            board.append(content)
    return values

def PrintBoard(board, length): # Clear the terminal and print the new board
    boardStr = ""
    for i, content in enumerate(board):
        if i % 16 == 0:
            boardStr += "\n"
        if content == "0":
            boardStr += colored("0", "red") + "   "
        elif content in ["+", "#"]:
            boardStr += colored(content, "green") + "   "
        else:
            if int(content) < 10:
                boardStr += content + "   "
            elif int(content) < 100:
                boardStr += content + "  "
            else:
                boardStr += colored("X", "blue") + "   "
    ClearScreen()
    print(boardStr)
    print(f"\nScore: {length-2}")

def CheckDeath(headPos, snakePos): # Check if the snake is outside of the board or intersecting itself
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True

    isOffScreen = not (0 < headPos[0] < 17) or not (0 < headPos[1] < 17)
    if isOffScreen:
        return True
    return False

def CheckPotentialDeath(newHeadPos, snakePos): # For a given input, check if the snake would die if it made that move
    if newHeadPos in snakePos:
        return True

    isOffScreen = not (0 < newHeadPos[0] < 17) or not (0 < newHeadPos[1] < 17)
    if isOffScreen:
        return True
    return False

def GenerateInput(direction, headPos, values): # Choose an appropriate input if possible and if not, choose a random one
    headNeighbors = GenerateNeighbors(headPos)
    inputValue = values[headNeighbors[0][0] + 16 * (headNeighbors[0][1] - 1) - 1]
    inputNeighbor = headNeighbors[0]
    for neighborPos in headNeighbors:
        neighborValue = values[neighborPos[0] + 16 * (neighborPos[1] - 1) - 1]
        if neighborValue < inputValue:
            inputValue = neighborValue
            inputNeighbor = neighborPos
    input = [inputNeighbor[0] - headPos[0], inputNeighbor[1] - headPos[1]]
    return input

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
        values = UpdateBoard(headPos, applePos, snakePos, board) # Update the board with all the fields
        PrintBoard(board, length) # Print the board to the terminal
        direction = GenerateInput(direction, headPos, values) # Update the direction with the generated one
        if direction == [2, 2]: # End the game if no more move is possible
            break
        wait(0.1) # Wait 0.2 seconds for visibility
    ClearScreen() # Clear the screen after losing
    print(f"You lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function