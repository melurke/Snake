# Import packages
import random
from time import sleep as wait
import pygame

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
            if pos == applePos:   content = "*" # Apple
            elif pos == headPos:  content = "#" # Head
            elif pos in snakePos: content = "+" # Body
            else:                 content = "O" # Empty field
            board.append(content)

def IndexToCoordinates(i):
    x = i % 16
    y = (i - i % 16) / 16
    x *= 50
    y *= 50
    return (x, y)

def PrintBoard(board, length, screen): # Clear the terminal and print the new board
    for i, content in enumerate(board):
        if content == "*":
            coords = IndexToCoordinates(i)
            AddRectangle(coords[0], coords[1], 255, 0, 0, screen)
        elif content == "#":
            coords = IndexToCoordinates(i)
            AddRectangle(coords[0], coords[1], 0, 255, 0, screen)
        elif content == "+":
            coords = IndexToCoordinates(i)
            AddRectangle(coords[0], coords[1], 0, 155, 0, screen)
        else:
            coords = IndexToCoordinates(i)
            AddRectangle(coords[0], coords[1], 0, 0, 0, screen)
    print(f"\nScore: {length-2}")
    pygame.display.update()

def CheckDeath(headPos, snakePos): # Check if the snake is outside of the board or intersecting itself
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True

    isOffScreen = not (0 < headPos[0] < 17) or not (0 < headPos[1] < 17)
    if isOffScreen:
        return True
    return False

def GenerateInput(headPos, rightPos, downPos, upPos, leftPos, direction):
    if headPos == [10, 9]:
        return [0, -1]
    if headPos in rightPos:
        return [1, 0]
    if headPos in leftPos:
        return [-1, 0]
    if headPos in upPos:
        return [0, -1]
    if headPos in downPos:
        return [0, 1]
    return direction

def AddRectangle(x, y, r, g, b, screen):
    pygame.draw.rect(screen, (r, g, b),(x+1, y+1, 48, 48))

def Main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Snake Game')
    
    length = 1
    applePos = [10, 9]
    headPos = [9, 9]
    snakePos = [headPos.copy()]
    direction = [1, 0]

    rightPos = [[1, 16], [2, 2], [3, 16], [4, 2], [5, 16], [6, 2], [7, 16], [8, 2], [9, 16], [10, 2], [11, 16], [12, 2], [13, 16], [14, 2], [15, 16]]
    upPos = [[2, 16], [4, 16], [6, 16], [8, 16], [10, 16], [12, 16], [14, 16], [16, 16]]
    leftPos = [[16, 1]]
    downPos = [[1, 1], [3, 2], [5, 2], [7, 2], [9, 2], [11, 2], [13, 2], [15, 2]]

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
        PrintBoard(board, length, screen) # Print the board to the terminal
        direction = GenerateInput(headPos, rightPos, downPos, upPos, leftPos, direction) # Generate a new direction randomly
        wait(0.005) # Wait a short amount of time for visibility
    print(f"\nYou lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function