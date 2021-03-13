# Copyright (c) 2021 David Sauer

from utils.visualisation import stone
import copy

SYMBOLS = ["✷", "◆", "✣", "✚", "●", "■"]
COLORS = ["R", "G", "O", "Y", "P", "B"]

class GameState:
    def __init__(self):
        self.playerA = Player(self)
        self.playerB = Player(self)
        self.playground = Playground(self)
        self.freeStones = StoneCollection(self, self)
        self.events = [] #controlled by controll class
        self.round = 0

class Playground:
    def __init__(self, game):
        self.game = game
        self.stones = StoneCollection(self, game, empty=True)
    def __str__(self):
        return str(self.stones)

class Player:
    def __init__(self, game):
        self.game = game
        self.stones = StoneCollection(self, game, empty=True)
    def __str__(self):
        return str(self.stones)

class StoneCollection:
    def __init__(self, parent, game, empty=False):
        self.parent = parent
        self.stones = []
        self.m = 0
        self.game = game
        if empty:
            return
        else:
            for symbol in SYMBOLS:
                for color in COLORS:
                    for n in range(3):
                        self.stones.append(Stone(self, symbol, color, n, self.m, self.game))
                        self.m += 1
    def remove(self, idx ):
        self.stones[idx].valid = False
    def append(self, item):
        self.stones.append(item)
        item.idx = self.m
        self.m += 1
    def __str__(self):
        output = ""
        n = -1
        for stone in list(self.stones):
            if stone.valid:
                n+=1
                if n%10 == 0 and n!=0:
                    output += "\n"
                output += str(stone) + "\t"
        return output

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
        return stone([self.symbol, self.color]) + "-{}".format(self.id)
    def move(self, to):
        if self.valid:
            to.append(copy.deepcopy(self))
            self.parent.remove(self.idx)

#TODO: Facilities for moving stones and printing stones, condition counting