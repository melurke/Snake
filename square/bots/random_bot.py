# Import packages
import random
from time import sleep as wait
import pygame

def ChooseApplePosition(snakePos, applePos, obstacles, portals): # Choose a new position for the apple after it is eaten
    pos = [random.randint(0, 15), random.randint(0, 15)]
    while pos in snakePos or pos in applePos or pos in obstacles or pos in portals:
        pos = [random.randint(0, 15), random.randint(0, 15)]
    return pos

def EatApple(headPos, snakePos, applePos, length, obstacles, portals): # Lengthen the snake if the apple is eaten and choose a new position for it
    if headPos in applePos:
        i = applePos.index(headPos)
        length += 1
        applePos[i] = ChooseApplePosition(snakePos, applePos, obstacles, portals)
        print(f"Score: {length - 2}")
    else:
        snakePos.remove(snakePos[0])
    return applePos, length

def UpdateBoard(headPos, applePos, snakePos, board, obstacles, portals): # Update all the fields on the board
    for y in range(0, 16):
        for x in range(0, 16):
            pos = [x, y]
            if pos in applePos:    content = "*"
            elif pos in portals:   content = "%"
            elif pos == headPos:   content = "#"
            elif pos in snakePos:  content = "+"
            elif pos in obstacles: content = "?"
            else:                  content = "O"
            board.append(content)

def IndexToCoordinates(i):
    x = i % 16
    y = (i - i % 16) / 16
    x *= 50
    y *= 50
    return (x, y)

def PrintBoard(board, screen, darkMode, portalUsed): # Clear the terminal and print the new board
    for i, content in enumerate(board):
        coords = IndexToCoordinates(i)
        if content == "*":
            AddRectangle(coords[0], coords[1], 255, 0, 0, screen)
        elif content == "#":
            AddRectangle(coords[0], coords[1], 0, 255, 0, screen)
        elif content == "+":
            AddRectangle(coords[0], coords[1], 0, 155, 0, screen)
        elif content == "%":
            if portalUsed:
                AddRectangle(coords[0], coords[1], 100, 155, 200, screen)
            else:
                AddRectangle(coords[0], coords[1], 100, 0, 200, screen)
        elif content == "?":
            if darkMode:
                AddRectangle(coords[0], coords[1], 255, 255, 255, screen)
            else:
                AddRectangle(coords[0], coords[1], 0, 0, 0, screen)
        else:
            if darkMode:
                AddRectangle(coords[0], coords[1], 0, 0, 0, screen)
            else:
                AddRectangle(coords[0], coords[1], 255, 255, 255, screen)
    pygame.display.update()

def CheckDeath(headPos, snakePos, obstacles): # Check if the snake is outside of the board or intersecting itself
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True
    if headPos in obstacles:
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
    numOfApples = 1
    obstacles = []
    portals = []
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
        applePos.append(ChooseApplePosition(snakePos, applePos, obstacles, portals))
    direction = [1, 0]

    while True:
        board = []
        # Update the position of the snake
        headPos[0] += direction[0]
        headPos[1] += direction[1]
        try:
            teleported = False
            if headPos == portals[0]:
                headPos = portals[1].copy()
                teleported = True
            if headPos == portals[1] and not teleported:
                headPos = portals[0].copy()
        except IndexError:
            pass
        snakePos.append(headPos.copy())
        portalUsed = False
        for pos in snakePos:
            if pos in portals:
                portalUsed = True
        applePos, length = EatApple(headPos, snakePos, applePos, length, obstacles, portals) # Update length and apple position

        if CheckDeath(headPos, snakePos, obstacles): # Check for death and end the game if neccessary
            break
        UpdateBoard(headPos, applePos, snakePos, board, obstacles, portals) # Update the board with all the new fields
        PrintBoard(board, screen, darkMode, portalUsed) # Print the board to the terminal
        direction = GenerateInput(snakePos, headPos) # Generate a new direction randomly
        wait(0.2) # Wait 0.2 seconds for visibility
    print(f"\nYou lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function