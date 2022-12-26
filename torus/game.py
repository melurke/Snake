# Import packages
import random
from time import sleep as wait
import pygame
import keyboard

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
            if pos in applePos:   content = "*"
            elif pos == headPos:  content = "#"
            elif pos in snakePos: content = "+"
            else:                 content = "O"
            board.append(content)
    return [board]

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

def AddRectangle(x, y, r, g, b, screen):
    pygame.draw.rect(screen, (r, g, b),(x + 1, y + 1, 48, 48))

def Main():
    numOfApples = 1

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Snake Game')

    length = 1
    headPos = [8, 8]
    snakePos = [headPos.copy()]
    applePos = [[9, 8]]
    for i in range(numOfApples-1):
        applePos.append(ChooseApplePosition(snakePos, applePos))
    direction = [1, 0]

    while True:
        board = []
        # Update the position of the snake
        headPos[0] += direction[0]
        headPos[1] += direction[1]
        headPos = [headPos[0] % 16, headPos[1] % 16]
        snakePos.append(headPos.copy())
        applePos, length = EatApple(headPos, snakePos, applePos, length) # Update length and apple position

        if CheckDeath(headPos, snakePos): # Check for death and end the game if neccessary
            break
        UpdateBoard(headPos, applePos, snakePos, board) # Update the board with all the new fields
        PrintBoard(board, screen) # Print the board to the terminal
        wait(0.2) # Wait for half a second so the player can't spam inputs
        direction = CheckInput(direction) # Check for player input and update the direction
    print(f"\nYou lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function