# Import packages
import random
from time import sleep as wait
import pygame

def ChooseApplePosition(snakePos): # Choose a new position for the apple after it is eaten
    pos = [random.randint(0, 15), random.randint(0, 15)]
    while pos in snakePos:
        pos = [random.randint(0, 15), random.randint(0, 15)]
    return pos

def EatApple(headPos, snakePos, applePos, length): # Lengthen the snake if the apple is eaten and choose a new position for it
    if headPos == applePos:
        length += 1
        applePos = ChooseApplePosition(snakePos)
        print(f"Score: {length - 2}")
    else:
        snakePos.remove(snakePos[0])
    return applePos, length

def UpdateBoard(headPos, applePos, snakePos, board): # Update all the fields on the board
    for y in range(0, 16):
        for x in range(0, 16):
            pos = [x, y]
            if pos == applePos:   content = "*"
            elif pos == headPos:  content = "#"
            elif pos in snakePos: content = "+"
            else:                 content = "O"
            board.append(content)

def IndexToCoordinates(i):
    x = i % 16
    y = (i - i % 16) / 16
    x *= 50
    y *= 50
    return (x, y)

def PrintBoard(board, screen): # Clear the terminal and print the new board
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

def GenerateInput(snakePos, headPos): # Make sure that the snake can't do a 180 turn and generate new inputs
    inputs = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    while inputs != []:
        input = random.choice(inputs)
        newHeadPos = [headPos[0] + input[0], headPos[1] + input[1]]
        if not newHeadPos in snakePos:
            return input
        inputs.remove(input)
    return random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])

def AddRectangle(x, y, r, g, b, screen):
    pygame.draw.rect(screen, (r, g, b),(x+1, y+1, 48, 48))

def Main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Snake Game')

    length = 1
    applePos = [9, 8]
    headPos = [8, 8]
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
        PrintBoard(board, screen) # Print the board to the terminal
        direction = GenerateInput(snakePos, headPos) # Generate a new direction randomly
        wait(0.2) # Wait 0.2 seconds for visibility
    print(f"\nYou lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function