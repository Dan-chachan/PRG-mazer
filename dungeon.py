import pygame

from utils import *
from setup import *


from random import randint

pygame.font.init()

tooltipFont = pygame.font.SysFont("Liberation Sans", 40, bold=1)



class Creature:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.hp = 0
        self.str = 0
        self.dex = 0

        self.defending = False

    def getAttacked(self, anAttack):
        dmg = anAttack[0]
        hitChance = anAttack[1] - self.dex/100

        chance = randint(0, 100)/100

        # hit
        if hitChance >= chance:
            if self.defending:
                self.hp -= dmg/2
        # else?

    # move to player?
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

class Orc(Creature):
    def __init__(self, maze, x, y):
        #super.__init__(self, x, y)
        self.x = x
        self.y = y

        self.hp = 40
        self.str = 20
        self.dex = 5

        # redundant?
        self.maze = maze

class Skeleton(Creature):
    def __init__(self, maze, x, y):
        #super.__init__(x, y)
        self.x = x
        self.y = y

        self.hp = 30
        self.str = 10
        self.dex = 10

        # redundant?
        self.maze = maze

class Slime(Creature):
    def __init__(self, maze, x, y):
        #super.__init__(self, x, y)
        self.x = x
        self.y = y

        self.hp = 20
        self.str = 5
        self.dex = 20

        # redundant?
        self.maze = maze


class Player(Creature):
    def __init__(self, maze, x, y):
        # redundant?
        # super.__init__()
        self.x = x
        self.y = y

        self.hp = 25
        self.str = 5
        self.dex = 5

        self.maze = maze

    def move(self, direction):
        coords = self.dir_to_coor(direction)

        if self.maze.isFree(coords):
            self.maze.place(coords, content["PLAYER"])
            self.maze.get((self.x, self.y)).remove(content["PLAYER"])
            self.setPos(coords)

    def setPos(self, coords):
        self.x = coords[0]
        self.y = coords[1]

    def attack(self):
        atType = input("[Q]UICK | [H]EAVY").lower()

        if atType == "q":
            dmgCoef = randint(7, 10) / 10
            hitChance = 1.0
        elif atType == "h":
            dmgCoef = randint(10, 13) / 10
            hitChance = 0.8
        else:
            print("You got confused!")
            dmgCoef = 0
            hitChance = 0

        anAttack = dmgCoef + self.str / 100, hitChance
        return anAttack


    def doBattle(self):
        # draw text
        action = input("What to do?\n", 
                        "[A]TTACK | [D]EFEND | [H]EAL | [F]LEE").lower()

        if action in "adhf":
            # do battle stuff
            return
        else:
            print("You got confused!")
        

class Maze:
    def __init__(self):
        self.size = MAZE_SIZE
        
        global content

        # redundant.
        #self.content = content

        self.board = []
        self.freeLocations = []
        self.baseLocations = []


        self.free = content["FREE"]
        self.exit = content["EXIT"]
        self.exitCoords = None

        self.entrance = content["ENTRY"]
        self.entryCoords = None


        # previous levels TODO
        self.pastLevels = ()

        self.player = None
        #self.init_player()

        self.new_level()

    def new_level(self):
        self.board = []
        self.freeLocations = []
        self.baseLocations = []
        self.create_board()
        self.create_maze()
        self.place_exits()
        self.init_player()
        self.getFreeLocations()
        print(self.freeLocations)
        self.place_enemies()
        # TODO self.pastLevels.append(board)
    # ~~~~~~~ INIT ~~~~~~~~
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
                while (toBuildOn.get() != content["WALL"]):
                    self.place(coords, content["WALL"])

                    x = x - 1 if build_dir == "left" else x + 1
                    coords = (x, y)
                    toBuildOn = self.get(coords)

            elif (build_dir in "updown"):
                while (toBuildOn.get() != content["WALL"]):
                    self.place(coords, content["WALL"])

                    y = y - 1 if build_dir == "up" else y + 1
                    coords = (x, y)
                    toBuildOn = self.get(coords)


            del self.baseLocations[builder]
            baseAmount -= 1

        return self.board
    
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

    def getFreeLocations(self):
        for y in range(0, self.size):
            for x in range(0, self.size):
                if self.get((x, y)).get() == content["FREE"]:
                    self.freeLocations.append((x, y))


    def init_player(self):
        if self.entryCoords is not None:

            x = self.entryCoords[0]
            y = self.entryCoords[1]
            
            self.place((x, y), content["PLAYER"])
            if self.player == None:
                self.player = Player(self, x, y)

            self.player.setPos((x, y))

            self.playerCoords = self.entryCoords
        else:
            print("Player could not be placed")
    
    def place_enemies(self, difficulty=0):
        global enemy

        for e in enemy.values():

            if e == enemy["ORC"]:
                minAmount = 0 + difficulty
                maxAmount = 2 + difficulty
            elif e == enemy["SKELETON"]:
                minAmount = 2 + difficulty
                maxAmount = 4
            elif e == enemy["SLIME"]:
                minAmount = 3 - difficulty if difficulty < 3 else 0
                maxAmount = 5 - difficulty if difficulty < 5 else 0
            # TODO make better!

            amount = randint(minAmount, maxAmount)
            spot = self.getRandFree()

            while (amount > 0):
                if e == enemy["ORC"]:
                    o = Orc(self, spot[0], spot[1])
                    self.place(spot, enemy["ORC"])

    # ~~~~~~~ INIT ~~~~~~~~
    def getRandFree(self):
        free = self.freeLocations[randint(0, len(self.freeLocations)-1)]
        return free


    def draw(self):
       
        # make automatic with classes?

        y = 0
        for row in self.board:
            x = 0
            for spot in row:
                color = RED
                spot = spot.get()
                
                if type(spot) == str:
                    if spot == content["WALL"]:
                        color = WALL_COL 
                    elif spot == content["FREE"]:
                        color = BACK_COL
                    elif spot == content["ENTRY"]:
                        color = ENTRY_COL
                    elif spot == content["EXIT"]:
                        color = EXIT_COL
                    elif spot == content["PLAYER"]:
                        color = PLAYER_COL
                   
                pygame.draw.rect(screen, color, 
                                 [x, y, GRID_SIZE, GRID_SIZE])

                x += GRID_SIZE
            y += GRID_SIZE


    def get(self, coords):
        if self.checkCoords(coords):
            x = coords[0]
            y = coords[1]

            return self.board[y][x]
        else:
            print("There is nothing here")
            return None

    def place(self, coords, thing):
        if (thing in content.values() and self.checkCoords(coords)):
            spot = self.get(coords)
            
            x = coords[0]
            y = coords[1]
            if spot is None:


                self.board[y][x] = Cell(x, y, thing)
            else:
                if thing is content["PLAYER"]:
                    self.playerCoords = (x, y)
                spot.add(thing)
        else:
            print("Thing can not be placed")


    def checkCoords(self, coords):
        xOk = coords[0] in range(0, self.size)
        yOk = coords[1] in range(0, self.size)

        return xOk and yOk

    def isFree(self, coords):
        if self.checkCoords(coords):
            #print("checking coords ", coords)
            toCheck = self.get(coords).get()

            if toCheck == content["WALL"]:
                return False
            elif toCheck == content["FREE"] or toCheck == content["EXIT"] or toCheck == content["ENTRY"]:
                return True
            # if enemy ...
        else:
            return False
    
    # TODO USELESS
    def movePlayer(self, coords):
        self.place(self.playerCoords, content["FREE"]) # bullshit
        self.place(coords, content["PLAYER"])

        self.playerCoords = coords

    def is_player_on(self, place):
        playerCoords = self.get(self.playerCoords).get(skipPlayer=True)

        # TODO nefunguje s ENTRY
        if playerCoords == place:
            return True
        else:
            return False

    def exitLevel(self):
        if self.is_player_on(content["EXIT"] or self.is_player_on(content["ENTRY"])):
            print("entering new level")
            self.new_level()

    def tooltipChecker(self):
        if self.playerCoords == self.exitCoords or self.playerCoords == self.entryCoords:
            tooltip = tooltipFont.render("[e]", 1, BLACK)
            
            textsize = tooltipFont.size("[e]")

            place = (WINDOW_WIDTH / 2 - textsize[0] / 2, GRID_SIZE/4)

            screen.blit(tooltip, place)

    #def battle(self, enemy):
    #    while (player.hp >= 0 and enemy.hp >= 0):
            

# TODO multiple things in one cell
class Cell:
    def __init__(self, x, y, c=content["FREE"]):
        self.content = [c]
        self.coords = (x, y)
    
    def add(self, newcont):
        # TODO redundant?
        if newcont in content.values():
            self.content.append(newcont)
        else:
            print("Invalid content")

    def remove(self, oldcont):
        if oldcont in self.content:
            self.content.remove(oldcont)

        if len(self.content) < 1:
            self.add(content["FREE"])

    def get(self, skipPlayer=False):
        if content["PLAYER"] in self.content:
            if skipPlayer:
                return self.content[-2]
            else:
                return content["PLAYER"]
        else:
            return self.content[-1]


from main import *