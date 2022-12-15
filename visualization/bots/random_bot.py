import random

def ChooseApplePosition(snakePos):
    pos = [random.randint(1, 16), random.randint(1, 16)]
    while pos in snakePos:
        pos = [random.randint(1, 16), random.randint(1, 16)]
    return pos

def EatApple(headPos, snakePos, applePos, length):
    if headPos == applePos:
        length += 1
        applePos = ChooseApplePosition(snakePos)
    else:
        snakePos.remove(snakePos[0])
    return applePos, length

def UpdateBoard(headPos, applePos, snakePos, board):
    board = []
    for y in range(1, 17):
        for x in range(1, 17):
            pos = [x, y]
            if pos == applePos:   content = 1
            elif pos == headPos:  content = 2
            elif pos in snakePos: content = 3
            else:                 content = 0
            board.append(content)
    return board

def CheckDeath(headPos, snakePos): # Check if the snake is outside of the board or intersecting itself
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True

    isOffScreen = not (0 < headPos[0] < 17) or not (0 < headPos[1] < 17)
    if isOffScreen:
        return True
    return False

def ChooseInput(): # Choose a random direction as the new one
    return random.choice([[1, 0], [-1, 0], [0, 1], [0, -1]])

def GenerateInput(direction): # Make shure that the snake can't do a 180 turn and generate new inputs
    input = ChooseInput()
    while input == [-1 * direction[0], -1 * direction[1]]:
        input = ChooseInput()
    return input

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
    applePos, length = EatApple(headPos, snakePos, applePos, length)

    if CheckDeath(headPos, snakePos): # Check for death and end the game if neccessary
        return []

    board = UpdateBoard(headPos, applePos, snakePos, board) # Update the board with all the new fields
    direction = GenerateInput(direction) # Generate a new direction randomly
    return [board, direction]