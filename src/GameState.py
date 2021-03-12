# Copyright (c) 2021 David Sauer

import numpy as np
from .utils.visualisation import stone

SYMBOLS = ["✷", "◆", "✣", "✚", "●", "■"]
COLORS = ["R", "G", "O", "Y", "P", "B"]

class GameState:
    def __init__(self):
        self.playerA = Player(self)
        self.playerB = Player(self)
        self.playground = Playground(self)
        self.freeStones = StoneCollection(self)
        self.events = [] #controlled by controll class
        self.round = 0

class Playground:
    def __init__(self, game):
        self.game = game
        self.stones = StoneCollection(self, game, empty=True)

class Player:
    def __init__(self, game):
        self.game = game
        self.stones = StoneCollection(self, game, empty=True)

class StoneCollection:
    def __init__(self, parent, game, empty=False):
        self.parent = parent
        self.stones = np.array()
        self.m = 0
        self.game = game
        if empty:
            return
        else:
            for symbol in SYMBOLS:
                for color in COLORS:
                    for n in range(3):
                        self.stones.append(Stone(parent, symbol, color, n, self.m, self.game))
                        self.m += 1
    def remove(self, idx ):
        self.stones[idx].valid = False
    def append(self, item):
        self.stones.append(item)
        item.idx = self.m
        self.m += 1

class Stone:
    def __init__(self, parent, symbol, color, id, idx, game):
        self.symbol = symbol
        self.color = color
        self.id = id
        self.parent = parent
        self.idx = idx
        self.valid = True
        self.game = game
    def __str__(self):
        return stone([self.symbol, self.color])
    def move(self, to):
        self.parent.remove(self.idx)
        to.append(self)

#TODO: Facilities for moving stones and printing stones, condition counting