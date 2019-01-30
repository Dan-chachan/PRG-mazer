import pygame

from utils import *
from setup import *


from random import randint

class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = "C"
        self.type = "undefined"

        self.hp = 0
        self.str = 0
        self.dex = 0

    def dir_to_coor(self, direction):
        x = self.x
        y = self.y
        if direction == 'U':
            y -= 1
        elif direction == 'D':
            y += 1
        elif direction == 'L':
            x -= 1
        elif direction == 'R':
            x += 1

        return (x, y)

class Player(Creature):
    def __init__(self, maze):
        self.x = None
        self.y = None

        self.hp = 25
        self.str = 5
        self.dex = 5

        self.sprite = "P"
        self.type = "player"

        self.maze = maze

    def move(self, direction):
        coords = self.dir_to_coor(direction)

        if self.maze.isFree(coords):
            self.maze.movePlayer(coords)

    def setPosition(self, coords):
        self.x = coords[0]
        self.y = coords[1]


class Maze:
    def __init__(self):
        self.size = MAZE_SIZE
        
        global content
        self.content = content

        self.board = []
        self.freeLocations = []
        self.baseLocations = []


        
        self.free = content["FREE"]
        self.exit = content["EXIT"]
        self.exitCoords = None

        self.entrance = content["ENTRY"]
        self.entryCoords = None

        # initialize the maze
        self.create_board()
        self.create_maze()
        self.place_exits()

        # previous levels
        self.currentLevel = self.board


        self.playerCoords = self.entryCoords
        self.player = Player(self)
        self.place_player()


    def create_board(self):
        for y in range(0, self.size):
            self.board.append([])

            for x in range(0, self.size):
                # walls on borders
                if y == 0 or y == self.size - 1 or x == 0 or x == self.size - 1:
                    self.board[y].append(Cell(x, y, content["WALL"]))

                # "bases" on certain locations
                elif y % 2 == 0 and x % 2 == 0: # TODO
                    self.board[y].append(Cell(x, y, content["BASE"]))
                    self.baseLocations.append((x, y))

                # free spots everywhere else
                else:
                    self.board[y].append(Cell(x, y))  

    def create_maze(self):
        DIRS = ["up", "down", "left", "right"]

        baseAmount = len(self.baseLocations)
        while (baseAmount != 0):

            # picking a random builder and a random direction
            builder = randint(0, baseAmount - 1)
            build_dir = DIRS[randint(0, 3)]

            coords = self.baseLocations[builder]
            x = coords[0]
            y = coords[1]

            # cell
            toBuildOn = self.get(coords)

            if (build_dir in "leftright"):                
                while (toBuildOn.content != content["WALL"]):
                    self.place(coords, content["WALL"])

                    x = x - 1 if build_dir == "left" else x + 1
                    coords = (x, y)
                    toBuildOn = self.get(coords)

            elif (build_dir in "updown"):
                while (toBuildOn.content != content["WALL"]):
                    self.place(coords, content["WALL"])

                    y = y - 1 if build_dir == "up" else y + 1
                    coords = (x, y)
                    toBuildOn = self.get(coords)


            del self.baseLocations[builder]
            baseAmount -= 1

        return self.board


    def draw(self):
       
        # make automatic with classes?

        y = 0
        for row in self.board:
            x = 0
            for spot in row:
                spot = spot.content
                if type(spot) == str:
                    if spot is content["WALL"]:
                        color = WALL_COL 
                    elif spot is content["FREE"]:
                        color = BACK_COL
                    elif spot is content["ENTRY"]:
                        color = ENTRY_COL
                    elif spot is content["EXIT"]:
                        color = EXIT_COL

                elif isinstance(spot, Player):
                    color = PLAYER_COL
                   
                pygame.draw.rect(screen, color, 
                                 [x, y, GRID_SIZE, GRID_SIZE])

                x += GRID_SIZE
            y += GRID_SIZE

    def place_exits(self):
        sz = self.size

        exitCoords = randint(0, 7)
        entryCoords = randint(0, 6)

        entryCoords = entryCoords if exitCoords != entryCoords else entryCoords+1
        
        possibleExits = (
            (1, 0), (sz-2, 0),          # first row
            (1, sz-1), (sz-2, sz-1),    # last row
            (0, 1), (sz-1, 1),          # second row
            (0, sz-2), (sz-1, sz-2)     # second to last row
        )

        # coordinants of the exit
        x = possibleExits[exitCoords][0]
        y = possibleExits[exitCoords][1]

        self.place((x, y), content["EXIT"])
        self.exitCoords = (x, y)

        # coordinants for the entrance
        x = possibleExits[entryCoords][0]
        y = possibleExits[entryCoords][1]

        self.place((x, y), content["ENTRY"])
        self.entryCoords = (x, y)

    # redundant?
    def place_player(self):
        if self.entryCoords is not None:
            x = self.entryCoords[0]
            y = self.entryCoords[1]
            
            self.place((x, y), content["PLAYER"])

            self.player.x = x
            self.player.y = y
        else:
            print("Player could not be placed")

    def get(self, coords):
        
        x = coords[0]
        y = coords[1]

        return self.board[y][x]

    def place(self, coords, thing):
        if thing in content.values():
            x = coords[0]
            y = coords[1]

            self.board[y][x] = Cell(x, y, thing)
        else:
            print("Thing can not be placed")


    def isFree(self, coords):
        if coords[0] <= self.size and coords[1] <= self.size:
            toCheck = self.get(coords)

            if toCheck is content["WALL"]:
                return False
            elif toCheck is content["FREE"]:
                return True
            # if enemy ...
        else:
            return False
    # playercoords?
    def movePlayer(self, coords):
        self.place(self.playerCoords, self.freeSpot)
        self.place(coords, self.player)

        self.player.setPosition(coords)


class Cell:
    def __init__(self, x, y, c = content["FREE"]):
        self.content = c

        self.coords = (x, y)

from main import *