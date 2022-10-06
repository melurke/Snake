import random
from time import sleep as wait
from termcolor import colored
import os

def ChooseApplePosition(snakePos):
    pos = [random.randint(1, 17), random.randint(1, 17)]
    while pos in snakePos:
        pos = [random.randint(1, 17), random.randint(1, 17)]
    return pos

def EatApple(headPos, snakePos, applePos, length):
    if headPos == applePos:
        length += 1
        applePos = ChooseApplePosition(snakePos)
    else:
        snakePos.remove(snakePos[0])
    return applePos, length

def UpdateBoard(headPos, applePos, snakePos, board):
    for y in range(1, 18):
        for x in range(1, 18):
            pos = [x, y]
            if pos == applePos:   content = "*"
            elif pos == headPos:  content = "#"
            elif pos in snakePos: content = "+"
            else:                 content = "O"
            board.append(content)

def PrintBoard(board):
    boardStr = ""
    for i, content in enumerate(board):
        if i % 17 == 0:
            boardStr += "\n"
        if content == "*":
            boardStr += "  " + colored(content, "red")
        elif content != "O":
            boardStr += "  " + colored(content, "green")
        else:
            boardStr += "  " + content
    print(boardStr)

def CheckDeath(headPos, snakePos):
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True

    isOffScreen = not (0 < headPos[0] < 18) or not (0 < headPos[1] < 18)
    if isOffScreen:
        return True
    return False

def CheckPotentialDeath(newHeadPos, snakePos):
    if newHeadPos in snakePos:
        return True

    isOffScreen = not (0 < newHeadPos[0] < 18) or not (0 < newHeadPos[1] < 18)
    if isOffScreen:
        return True
    return False

def GenerateInput(direction, applePos, headPos, snakePos):
    choices = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    input = ChooseInput(applePos, headPos, direction, snakePos)
    while not ValidateInput(input, direction, headPos, snakePos):
        if len(choices) > 0:
            input = random.choice(choices)
            choices.remove(input)
        else:
            return [2, 2]
    return input

def ValidateInput(input, direction, headPos, snakePos):
    if input == [-1 * direction[0], -1 * direction[1]] or CheckPotentialDeath([headPos[0] + input[0], headPos[1] + input[1]], snakePos):
        return False
    return True

def ChooseInput(applePos, headPos, direction, snakePos):
    input = [0, 0]
    if applePos[0] < headPos[0]:
        input[0] = -1
    elif applePos[0] > headPos[0]:
        input[0] = 1
    else:
        if applePos[1] < headPos[1]:
            input[1] = -1
        elif applePos[1] > headPos[1]:
            input[1] = 1
    if not ValidateInput(input, direction, headPos, snakePos):
        input = [0, 0]
        if applePos[1] < headPos[1]:
            input[1] = -1
        elif applePos[1] > headPos[1]:
            input[1] = 1
        else:
            if applePos[0] < headPos[0]:
                input[0] = -1
            elif applePos[0] > headPos[0]:
                input[0] = 1
    return input

def Main():
    os.system('cls' if os.name == 'nt' else 'clear')

    length = 1
    applePos = [10, 9]
    headPos = [9, 9]
    snakePos = [headPos.copy()]
    direction = [1, 0]

    while True:
        board = []
        headPos[0] += direction[0]
        headPos[1] += direction[1]
        snakePos.append(headPos.copy())
        applePos, length = EatApple(headPos, snakePos, applePos, length)

        if CheckDeath(headPos, snakePos):
            break
        UpdateBoard(headPos, applePos, snakePos, board)
        PrintBoard(board)
        direction = GenerateInput(direction, applePos, headPos, snakePos)
        if direction == [2, 2]:
            break
        wait(0.2)
        os.system('cls' if os.name == 'nt' else 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"You lost! Your score was {length-2}")
    return length-2

if __name__ == '__main__':
    Main()