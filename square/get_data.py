# Import packages
import random
import matplotlib.pyplot as plt

# Import generation functions from all the bots
from bots.dijkstra_bot import GenerateInput, GenerateDijkstraValues

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
    else:
        snakePos.remove(snakePos[0])
    return applePos, length

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
    numOfApples = 1
    obstacles = []
    portals = []
    
    length = 1
    headPos = [8, 8]
    snakePos = [headPos.copy()]
    applePos = [[9, 8]]
    for i in range(numOfApples-1):
        applePos.append(ChooseApplePosition(snakePos, applePos, obstacles, portals))
    direction = [1, 0]

    while True:
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
        applePos, length = EatApple(headPos, snakePos, applePos, length, obstacles, portals) # Update length and apple position

        if CheckDeath(headPos, snakePos, obstacles): # Check for death and end the game if neccessary
            break
        values = GenerateDijkstraValues(applePos, snakePos, obstacles, portals)
        direction = GenerateInput(headPos, values) # Update the direction with the generated one
        if direction == [2, 2]: # End the game if no more move is possible
            break
    return length - 2

def Main():
    numOfGames = 100000
    games = RunGames(numOfGames)
    average, distribution = ProcessGames(games)
    SaveResults(numOfGames, average, distribution, "../data/dijkstra_bot/square/results.txt")

if __name__ == '__main__':
    try:
        Main() # Run the main function
    except:
        pass