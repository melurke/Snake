import pygame as pg
import random

pg.init()
screen = pg.display.set_mode((800, 800))
pg.display.set_caption("Snake")

board = []
for i in range(256):
    board.append(random.randint(0, 3))

def BoardToColor(boardStr):
    if boardStr == 0:
        return (10, 10, 10)
    elif boardStr == 1:
        return (200, 0, 0)
    elif boardStr == 2:
        return (0, 200, 0)
    elif boardStr == 3:
        return (0, 100, 0)
    else:
        return (0, 0, 0)

def IndexToCoordinates(i):
    x = i % 16
    y = (i - i % 16) / 16
    x *= 50
    y *= 50
    return (x, y)

def PrintField(x, y, color):
    pg.draw.rect(screen, color, (x, y, 50, 50))

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    for i, x in enumerate(board):
        coordinates = IndexToCoordinates(i)
        color = BoardToColor(x)
        PrintField(coordinates[0], coordinates[1], color)
    pg.display.update()