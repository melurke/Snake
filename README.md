# Snake

In this repository, I created the game Snake to play in the terminal and some different bots that play the game automatically.

## Bots

To get the data for the bots, I used get_data.py. The program runs a certain amount of games (mostly 1 million) and stores the results in a text file.
To see the exact number of games where the snake scored a certain number of points, see data folder and the results file in the folder for each bot.

### Random Bot

The random bot is pretty simple: The snake does a random possible move every turn. That's it.

#### Data

Average: 0.137394

Histogram:
<img src="data/random_bot/histogram.png">

We can see, that the bot doesn't do that well, but it did score 5 once, so that's more than I expected.

### Simple Bot

The simple bot tries to get closer to the apple, firstly in the horizontal direction and then in the vertical direction. If the snake can't get closer in either direction, it makes a random move.

#### Data

Average: 25.150566

Histogram:
<img src="data/simple_bot/histogram.png">

The score is much more widely spread, with the record being a score of 75, scored twice.
For some reason, the bot seems to score even numbers of scores much more that odd ones. I unfortunately don't know why that is, but it seems important to point it out.


### Dijkstra Bot

The Dijkstra Bot uses the Dijkstra Algorithm, that counts the number of steps it takes to get to the apple for each field and lets the snake move to the smallest number near it. The numbers are also printed on the field while the bot is playing, so it is easier to see which path the bot is following.

I'm planning to improve the bot so it tries to avoid moves that enclose a large area, so the bot doesn't get trapped as often.

#### Data

/!\ Not yet implemented /!\