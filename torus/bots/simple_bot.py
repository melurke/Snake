# Import packages
import random
from time import sleep as wait
import pygame

def ChooseApplePosition(snakePos, applePos, obstacles): # Choose a new position for the apple after it is eaten
    pos = [random.randint(0, 15), random.randint(0, 15)]
    while pos in snakePos or pos in applePos or pos in obstacles:
        pos = [random.randint(0, 15), random.randint(0, 15)]
    return pos

def EatApple(headPos, snakePos, applePos, length, i, obstacles): # Lengthen the snake if the apple is eaten and choose a new position for it
    newApple = i
    if headPos in applePos:
        length += 1
        i = applePos.index(headPos)
        applePos[i] = ChooseApplePosition(snakePos, applePos, obstacles)
        newApple = GenerateClosestApple(applePos, headPos)
        print(f"Score: {length - 2}")
    else:
        snakePos.remove(snakePos[0])
    return applePos, length, newApple

def AppleDistance(headPos, applePos):
    if abs(headPos[0] - applePos[0]) < 8:
        x = abs(headPos[0] - applePos[0])
    else:
        x = 8 - (abs(headPos[0] - applePos[0]) % 8)
    if abs(headPos[1] - applePos[1]) < 8:
        y = abs(headPos[1] - applePos[1])
    else:
        y = 8 - (abs(headPos[1] - applePos[1]) % 8)
    return x + y

def GenerateClosestApple(applePos, headPos):
    dist = []
    for pos in applePos:
        dist.append(AppleDistance(headPos, pos))

    return dist.index(min(dist))

def UpdateBoard(headPos, applePos, snakePos, board, obstacles): # Update all the fields on the board
    for y in range(0, 16):
        for x in range(0, 16):
            pos = [x, y]
            if pos in applePos:    content = "*"
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

def PrintBoard(board, screen, darkMode): # Clear the terminal and print the new board
    for i, content in enumerate(board):
        coords = IndexToCoordinates(i)
        if content == "*":
            AddRectangle(coords[0], coords[1], 255, 0, 0, screen)
        elif content == "#":
            AddRectangle(coords[0], coords[1], 0, 255, 0, screen)
        elif content == "+":
            AddRectangle(coords[0], coords[1], 0, 155, 0, screen)
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

def CheckDeath(headPos, snakePos): # Check if the snake is outside of the board or intersecting itself
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True

def CheckPotentialDeath(newHeadPos, snakePos, obstacles): # For a given input, check if the snake would die if it made that move
    if newHeadPos in snakePos or newHeadPos in obstacles:
        return True

def ChooseInput(applePos, headPos, direction, snakePos, obstacles): # Choose the input that would get the snake closest to the apple
    input = [0, 0]
    if applePos[0] < headPos[0]:
        if headPos[0] - applePos[0] > 8:
            input[0] = 1
        else:
            input[0] = -1
    elif applePos[0] > headPos[0]:
        if applePos[0] - headPos[0] > 8:
            input[0] = -1
        else:
            input[0] = 1
    else:
        if applePos[1] < headPos[1]:
            if headPos[1] - applePos[1] > 8:
                input[1] = 1
            else:
                input[1] = -1
        elif applePos[1] > headPos[1]:
            if applePos[1] - headPos[1] > 8:
                input[1] = -1
            else:
                input[1] = 1
    if not ValidateInput(input, direction, headPos, snakePos, obstacles):
        input = [0, 0]
        if applePos[1] < headPos[1]:
            if headPos[1] - applePos[1] > 8:
                input[1] = 1
            else:
                input[1] = -1
        elif applePos[1] > headPos[1]:
            if applePos[1] - headPos[1] > 8:
                input[1] = -1
            else:
                input[1] = 1
        else:
            if applePos[0] < headPos[0]:
                if headPos[0] - applePos[0] > 8:
                    input[0] = 1
                else:
                    input[0] = -1
            elif applePos[0] > headPos[0]:
                if applePos[0] - headPos[0] > 8:
                    input[0] = -1
                else:
                    input[0] = 1
    return input

def GenerateInput(direction, applePos, headPos, snakePos, obstacles): # Choose an appropriate input if possible and if not, choose a random one
    choices = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    input = ChooseInput(applePos, headPos, direction, snakePos, obstacles)
    while not ValidateInput(input, direction, headPos, snakePos, obstacles):
        if len(choices) > 0:
            input = random.choice(choices)
            choices.remove(input)
        else:
            return [2, 2]
    return input

def ValidateInput(input, direction, headPos, snakePos, obstacles): # Make shure the snake doesn't do a 180 turn or would die for a given input
    if input == [-1 * direction[0], -1 * direction[1]] or CheckPotentialDeath([headPos[0] + input[0], headPos[1] + input[1]], snakePos, obstacles):
        return False
    return True

def AddRectangle(x, y, r, g, b, screen):
    pygame.draw.rect(screen, (r, g, b),(x+1, y+1, 48, 48))

def Main():
    numOfApples = 1
    obstacles = []
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
    appleIndex = 0
    for i in range(numOfApples-1):
        applePos.append(ChooseApplePosition(snakePos, applePos, obstacles))
    direction = [1, 0]

    while True:
        board = []
        # Update the position of the snake
        headPos[0] += direction[0]
        headPos[1] += direction[1]
        headPos = [headPos[0] % 16, headPos[1] % 16]
        snakePos.append(headPos.copy())
        applePos, length, appleIndex = EatApple(headPos, snakePos, applePos, length, appleIndex, obstacles) # Update length and apple position

        if CheckDeath(headPos, snakePos): # Check for death and end the game if neccessary
            break
        UpdateBoard(headPos, applePos, snakePos, board, obstacles) # Update the board with all the fields
        PrintBoard(board, screen, darkMode) # Print the board to the terminal
        direction = GenerateInput(direction, applePos[appleIndex], headPos, snakePos, obstacles) # Update the direction with the generated one
        if direction == [2, 2]: # End the game if no more move is possible
            break
        wait(0.1) # Wait 0.2 seconds for visibility
    print(f"You lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function