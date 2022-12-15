# Import packages
import random

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
            if pos == applePos:   content = 1
            elif pos == headPos:  content = 2
            elif pos in snakePos: content = 3
            else:                 content = 0
            board.append(content)
    return [board]

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

def ChooseInput(applePos, headPos, direction, snakePos): # Choose the input that would get the snake closest to the apple
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

def GenerateInput(direction, applePos, headPos, snakePos): # Choose an appropriate input if possible and if not, choose a random one
    choices = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    input = ChooseInput(applePos, headPos, direction, snakePos)
    while not ValidateInput(input, direction, headPos, snakePos):
        if len(choices) > 0:
            input = random.choice(choices)
            choices.remove(input)
        else:
            return [2, 2]
    return input

def ValidateInput(input, direction, headPos, snakePos): # Make shure the snake doesn't do a 180 turn or would die for a given input
    if input == [-1 * direction[0], -1 * direction[1]] or CheckPotentialDeath([headPos[0] + input[0], headPos[1] + input[1]], snakePos):
        return False
    return True

def IndexToCoordinates(i):
    x = i % 16
    y = (i - i % 16) / 16
    return [x, y]

def AnalyseBoard(board):
    apple = []
    head = []
    snake = []

    for i, x in board:
        if x == 1:
            apple = IndexToCoordinates(i)
        elif x == 2:
            head = IndexToCoordinates(i)
            snake.append(IndexToCoordinates(i))
        elif x == 3:
            snake.append(IndexToCoordinates(i))
    return apple, head, snake

def Main(board, direction):

    applePos, headPos, snakePos = AnalyseBoard(board)

    headPos[0] += direction[0]
    headPos[1] += direction[1]
    snakePos.append(headPos.copy())
    applePos, length = EatApple(headPos, snakePos, applePos, length) # Update length and apple position

    if CheckDeath(headPos, snakePos): # Check for death and end the game if neccessary
        return []
    board = UpdateBoard(headPos, applePos, snakePos, board) # Update the board with all the fields
    direction = GenerateInput(direction, applePos, headPos, snakePos) # Update the direction with the generated one
    if direction == [2, 2]: # End the game if no more move is possible
        return []
    return [board, direction]