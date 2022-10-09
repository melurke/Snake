# Import packages
import random
import matplotlib.pyplot as plt

# Import generation functions from all the bots
from bots.simple_bot import GenerateInput

def ChooseApplePosition(snakePos): # Choose a new position for the apple after it is eaten
    pos = [random.randint(1, 17), random.randint(1, 17)]
    while pos in snakePos:
        pos = [random.randint(1, 17), random.randint(1, 17)]
    return pos

def EatApple(headPos, snakePos, applePos, length): # Lengthen the snake if the apple is eaten and choose a new position for it
    if headPos == applePos:
        length += 1
        applePos = ChooseApplePosition(snakePos)
    else:
        snakePos.remove(snakePos[0])
    return applePos, length

def CheckDeath(headPos, snakePos): # Check if the snake is outside of the board or intersecting itself
    bodyPos = snakePos.copy()
    bodyPos.remove(headPos)
    if headPos in bodyPos:
        return True

    isOffScreen = not (0 < headPos[0] < 18) or not (0 < headPos[1] < 18)
    if isOffScreen:
        return True
    return False

def RunGames(numOfGames):
    games = []
    for i in range(numOfGames):
        print(i)
        games.append(Game())
    return games

def ProcessData(games):
    distribution = [0] * (max(games)+1)
    for game in games:
        distribution[game] += 1
    average = Average(distribution)
    return average, distribution

def Average(distribution):
    expectedValue = 0
    numOfGames = 0
    for index, score in enumerate(distribution):
        expectedValue += index * score
        numOfGames += score
    expectedValue /= numOfGames
    return expectedValue

def ProcessGames(games):
    average, distribution = ProcessData(games)
    print(average)
    print(distribution)
    xValues = []
    for i in range(len(distribution)):
        xValues.append(i)
    plt.bar(xValues, height=distribution)
    plt.show()
    return average, distribution

def SaveResults(numOfGames, average, distribution, fileLocation):
    string = f"Average: {average}\n\nScores:\n"
    for index, value in enumerate(distribution):
        string += f"{index}: {value}\n"
    string += f"\nTotal: {numOfGames}"
    WriteToFile(string, fileLocation)

def WriteToFile(string, fileLocation):
    with open(fileLocation, "w") as file:
        file.write(string)

def Game(): # Play one game at a time
    length = 1
    applePos = [10, 9]
    headPos = [9, 9]
    snakePos = [headPos.copy()]
    direction = [1, 0]

    while True:
        # Update the position of the snake
        headPos[0] += direction[0]
        headPos[1] += direction[1]
        snakePos.append(headPos.copy())
        applePos, length = EatApple(headPos, snakePos, applePos, length) # Update length and apple position

        if CheckDeath(headPos, snakePos): # Check for death and end the game if neccessary
            break
        direction = GenerateInput(direction, applePos, headPos, snakePos) # Update the direction with the generated one
        if direction == [2, 2]: # End the game if no more move is possible
            break
    return length - 2

def Main():
    numOfGames = 100000
    games = RunGames(numOfGames)
    average, distribution = ProcessGames(games)
    SaveResults(numOfGames, average, distribution, "data/simple_bot/results.txt")

if __name__ == '__main__':
    Main() # Run the main function