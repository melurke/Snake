# Import packages
import random
from time import sleep as wait
import pygame

def ChooseApplePosition(snakePos, applePos): # Choose a new position for the apple after it is eaten
    pos = [random.randint(0, 15), random.randint(0, 15)]
    while pos in snakePos or pos in applePos:
        pos = [random.randint(0, 15), random.randint(0, 15)]
    return pos

def EatApple(headPos, snakePos, applePos, length): # Lengthen the snake if the apple is eaten and choose a new position for it
    if headPos in applePos:
        i = applePos.index(headPos)
        length += 1
        applePos[i] = ChooseApplePosition(snakePos, applePos)
        print(f"Score: {length - 2}")
    else:
        snakePos.remove(snakePos[0])
    return applePos, length

def UpdateBoard(headPos, applePos, snakePos, board): # Update all the fields on the board
    for y in range(0, 16):
        for x in range(0, 16):
            pos = [x, y]
            if pos in applePos:   content = "*" # Apple
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

def PrintBoard(board, screen, darkMode): # Clear the terminal and print the new board
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
            if darkMode:
                AddRectangle(coords[0], coords[1], 0, 0, 0, screen)
            else:
                AddRectangle(coords[0], coords[1], 255, 255, 255, screen)
    pygame.display.update()

def CheckDeath(headPos, snakePos): # Check if the snake is outside of the board or intersecting itself
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True

    isOffScreen = not (-1 < headPos[0] < 16) or not (-1 < headPos[1] < 16)
    if isOffScreen:
        return True
    return False

def GenerateInput(headPos, rightPos, downPos, upPos, leftPos, direction):
    if headPos == [9, 8]:
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
    numOfApples = 1
    darkMode = False

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Snake Game')
    if darkMode:
        screen.fill((200, 200, 200))
    
    length = 1
    headPos = [8, 8]
    snakePos = [headPos.copy()]
    applePos = [[9, 8]]
    for i in range(numOfApples-1):
        applePos.append(ChooseApplePosition(snakePos, applePos))
    direction = [1, 0]

    rightPos = [[0, 15], [1, 1], [2, 15], [3, 1], [4, 15], [5, 1], [6, 15], [7, 1], [8, 15], [9, 1], [10, 15], [11, 1], [12, 15], [13, 1], [14, 15]]
    upPos = [[1, 15], [3, 15], [5, 15], [7, 15], [9, 15], [11, 15], [13, 15], [15, 15]]
    leftPos = [[15, 0]]
    downPos = [[0, 0], [2, 1], [4, 1], [6, 1], [8, 1], [10, 1], [12, 1], [14, 1]]

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
        PrintBoard(board, screen, darkMode) # Print the board to the terminal
        direction = GenerateInput(headPos, rightPos, downPos, upPos, leftPos, direction) # Generate a new direction randomly
        wait(0.005) # Wait a short amount of time for visibility
    print(f"\nYou lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function