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

def ValidNeighbor(pos):
    if not (-1 < pos[0] < 16):
        return False
    if not (-1 < pos[1] < 16):
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
    fields = applePos.copy()
    for pos in applePos:
        values[pos[0] + 16 * pos[1] - 17] = 0
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
    for pos in applePos:
        values[pos[0] + 16 * (pos[1] - 1) - 1] = 0
    return values

def UpdateBoard(headPos, applePos, snakePos, board): # Update all the fields on the board
    values = GenerateDijkstraValues(applePos, snakePos)
    for y in range(0, 16):
        for x in range(0, 16):
            pos = [x, y]
            if pos in applePos:   content = "*"
            elif pos == headPos:  content = "#"
            elif pos in snakePos: content = "+"
            else:                 content = str(values[x + 16 * (y - 1) - 1])
            board.append(content)
    return values

def Clamp(min, value, max):
    if value < min:
        return min
    if value > max:
        return max
    return value

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
            AddRectangle(coords[0], coords[1], (255-(Clamp(0, 20 * int(content), 255))), 255-(Clamp(0, 15 * int(content), 255)), 255-(Clamp(0, 15 * int(content), 255)), screen)
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

def CheckPotentialDeath(newHeadPos, snakePos): # For a given input, check if the snake would die if it made that move
    if newHeadPos in snakePos:
        return True

    isOffScreen = not (-1 < newHeadPos[0] < 16) or not (-1 < newHeadPos[1] < 16)
    if isOffScreen:
        return True
    return False

def GenerateInput(headPos, values): # Choose an appropriate input if possible and if not, choose a random one
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

def AddRectangle(x, y, r, g, b, screen):
    pygame.draw.rect(screen, (r, g, b),(x+1, y+1, 48, 48))

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
        snakePos.append(headPos.copy())
        applePos, length = EatApple(headPos, snakePos, applePos, length) # Update length and apple position

        if CheckDeath(headPos, snakePos): # Check for death and end the game if neccessary
            break
        values = UpdateBoard(headPos, applePos, snakePos, board) # Update the board with all the fields
        PrintBoard(board, screen) # Print the board to the terminal
        direction = GenerateInput(headPos, values) # Update the direction with the generated one
        if direction == [2, 2]: # End the game if no more move is possible
            break
        wait(0.1) # Wait 0.2 seconds for visibility
    print(f"You lost! Your score was {length-2}") # Print the score after the game is lost

if __name__ == '__main__':
    Main() # Run the main function