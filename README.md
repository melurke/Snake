# Snake

In this repository, we created the game Snake to play in the terminal and some different bots that play the game automatically.

## Bots

To get the data for the bots, we used get_data.py. The program runs a certain amount of games (mostly 1 million) and stores the results in a text file.
To see the exact number of games where the snake scored a certain number of points, see data folder and the results file in the folder for each bot.


### Random Bot

The random bot is pretty simple: The snake performs a random possible move every turn. That's it.

#### Square

Average: 0.137394

Histogram:
<img src="data/random_bot/square/histogram.png">

One can see that the bot doesn't do that well, but it did score 5 once, so that's more than we expected.

#### Torus

Average: 7.584119

Histogram:
<img src="data/random_bot/torus/histogram.png">

Now that the bot can't die by running into a wall, the minimum score is 6. With that length it is possible for the snake to surround itself and die. After that, the score drops pretty fast though. Still, the average is pretty high for a bot that only performs random moves.


### Simple Bot

The simple bot tries to get closer to the apple, firstly in the horizontal direction and then in the vertical direction. If the snake can't get closer in either direction, it makes a random move.

#### Square

Average: 25.150566

Histogram:
<img src="data/simple_bot/square/histogram.png">

This data follows a bell curve slightly tilted to the left. Our theory is that the probability of dying is low at the beginning and then rises with the score. So there are few games with a low score and few games with a high score because the bot was likely to die beforehand.

#### Torus

Average: 24.572957

Histogram:
<img src="data/simple_bot/torus/histogram.png">

For the torus the bot also follows a bell curve. What's surprising is that the average is lower than that of the square. But the scores are also more widely spread with the highest score being 88 instead of 75.


### Dijkstra Bot

The Dijkstra Bot uses the Dijkstra Algorithm, that counts the number of steps it takes to get to the apple for each field and lets the snake move to the smallest number near it. This is also represented on the field with a color gradient indicating where the snake wants to go.

#### Square

Average: 48.84104

Histogram:
<img src="data/dijkstra_bot/square/histogram.png">

Unlike the simple bot, the plot of this bot seems to be tilted to the right. This bot also performs the best of all the bots in the square field (excluding the hamiltonian bot). With a top score of 105 it filled up more than 40% of the field.

#### Torus

Average: 63.53288

Histogram:
<img src="data/dijkstra_bot/torus/histogram.png">

This is by far the best bot (except for the hamiltonian bot). With a high score of 130 it filled up more than half of the field. Like the other graph, this bell curve is also tilted to the right.


### Hamiltonian Bot

The Hamiltonian Bot follows a simple Hamiltonian Cycle and thus always scores 253, the maximum possible score in (our version of) the game.
It is most certainly not the most efficient bot accounting for the number of steps taken, but the absolute score is optimal.


## What's up for the future?

In the future, we want to gather data for the bots using a different number of apples, obstacles and portals. We're excited to see how those extra variables affect the results of the different bots.
We're also working on a perfect bot that scores the highest (also accounting for the number of steps taken).
Another plan is implementing a multiplayer mode, where the player can battle against a bot in the same field, in a different field, or where two players can play against each other.
A big project for the future is adding documentation including pictures and gifs to a website, so the project is more accessible. This also includes a version of the game to play in the browser.