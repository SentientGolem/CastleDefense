from PIL import Image, ImageTk
from math import ceil, floor
from random import randint, choice

class mapGen():
    def __init__(self, master):
        self.master = master
        self.tileSize = 20
        self.setPictures()
        self.generateBoard()
        # Did the dumb, self.board is also used for the ASCII 
        # layout of the board and then I reassigned it here 
        # and used it multiple time through the files.
        # Gonna save it with a new variable, bad planning
        self.boardASCII = self.board
        self.board = self.setBoard()

    def setPictures(self):
        self.castle = Image.open('Images/Castle.jpg').resize((self.tileSize, self.tileSize))
        self.forest = Image.open('Images/treeJeff3.png').resize((self.tileSize, self.tileSize))
        self.plains = Image.open('Images/plainsJeff2.png').resize((self.tileSize, self.tileSize))
        self.silverMine = Image.open('Images/SilverMine.jpg').resize((self.tileSize, self.tileSize))
        self.stoneDeposit = Image.open('Images/StoneDeposit.jpg').resize((self.tileSize, self.tileSize))
        self.mountain = Image.open('Images/Mountain.png').resize((self.tileSize, self.tileSize))
        self.metal = Image.open('Images/metal.png').resize((self.tileSize, self.tileSize))

    def generateBoard(self):
        self.plainsCode = 'p000'
        self.forestCode = 'f000'
        self.stoneCode = 'q000'
        self.silverCode = 's000'
        self.metalCode = 'm000'
        self.mountainCode = 'v000'
        self.castleCode = 'c000'
        # Makes a list of lists
        self.board = []
        self.boardSize = 100
        for x in range(self.boardSize):
            self.board.append([self.plainsCode] * self.boardSize)

        # Gets entire map size 
        self.mapSize = len(self.board) * len(self.board[0])

        # This is to keep track of what changes in every iteration
        self.changed = []
        self.addForest()
        self.addMountain()
        self.addSilver()
        self.addQuarries()
        self.addMetal()

    def addMountain(self):
        # First we need math to figure out how many mountain seeds we want
        # Every seed will grow a random number of mountains nearby
        # For every 100 tiles, there will be 1 mountain seed +- 1
        self.mountainSeed = ceil(self.mapSize/10) + randint(floor(self.mapSize / -100), floor(self.mapSize / 100))
        print('Mountain Seeds ', self.mountainSeed)
        self.seedMountain()
        self.allMountains = []
        while self.mountainSeed >= 1:
            self.seed = randint(0, 9)
            if self.seed == 0:
                self.seedMountain()
            else:
                self.allMountains.clear()
                self.findFeature()
                self.placeMountain()
        print('All Mountains: ', len(self.allMountains))

    def seedMountain(self):
        # Picks random coordinate for new mountain seed
        self.rand1 = randint(0, (len(self.board) - 1))
        self.rand2 = randint(0, (len(self.board) - 1))
        # Doesn't need to check for a plains
        if self.board[self.rand1][self.rand2] != self.mountainCode:
            self.placeSeedMountain(self.rand1, self.rand2)
            self.mountainSeed -= 1

    def placeSeedMountain(self, y, x):
        self.board[y][x] = self.mountainCode
        loop = True
        while loop == True:
            trail = randint(1, 8)
            # 1 is South
            if trail == 1 and y < self.boardSize - 1:
                self.board[y + 1][x] = self.mountainCode
                loop = False
                return
            # 2 is South East
            elif trail == 2 and y < self.boardSize - 1 and x < self.boardSize - 1:
                self.board[y + 1][x + 1] = self.mountainCode
                loop = False
                return
            # 3 is East
            elif trail == 3 and x < self.boardSize - 1:
                self.board[y][x + 1] = self.mountainCode
                loop = False
                return
            # 4 is North East
            elif trail == 4 and y > 0 and x < self.boardSize - 1:
                self.board[y - 1][x + 1] = self.mountainCode
                loop = False
                return
            # 5 is North
            elif trail == 5 and y > 0:
                self.board[y - 1][x] = self.mountainCode
                loop = False
                return
            # 6 is North West
            elif trail == 6 and y > 0 and x > 0:
                self.board[y - 1][x - 1] = self.mountainCode
                loop = False
                return
            # 7 is West
            elif trail == 7 and x > 0:
                self.board[y][x-1] = self.mountainCode
                loop = False
                return
            # 8 is South West
            elif trail == 8 and y < self.boardSize - 1 and x > 0:
                self.board[y + 1][x - 1] = self.mountainCode
                loop = False
                return

    def findFeature(self):
        # Begins iterating through the board
        for idy, row in enumerate(self.board):
            for idx, column in enumerate(self.board[idy]):
                # When we find a tile that is a forest
                if self.board[idy][idx] == self.forestCode:
                    self.allForests.append([idy, idx])
                elif self.board[idy][idx] == self.mountainCode:
                    self.allMountains.append([idy,idx])

    def placeMountain(self):
        self.mountainCoordinates = choice(self.allMountains)
        idy = self.mountainCoordinates[0]
        idx = self.mountainCoordinates[1]
        # Needs to check surroundings for other mountains
        surroundings = []
        # Needs to make sure the center point isn't on any edges
        if idy != self.boardSize - 1 and idy != 0 and idx != self.boardSize - 1 and idx != 0:
            # Checks if there is a mountain to the South
            if self.board[idy + 1][idx] == self.mountainCode:
                if self.seed >= 1 and self.seed <= 3:
                    # Adds a mountain NW
                    surroundings.append([idy - 1, idx - 1])
                elif self.seed >= 4 and self.seed <= 6:
                    # Adds N
                    surroundings.append([idy - 1, idx])
                elif self.seed >= 7 and self.seed <= 9:
                    # Adds NE
                    surroundings.append([idy - 1, idx + 1])
            # Checks if there is a mountain to the South East
            if self.board[idy + 1][idx + 1] == self.mountainCode:
                if self.seed >= 1 and self.seed <= 3:
                    # Adds West
                    surroundings.append([idy, idx - 1])
                elif self.seed >= 4 and self.seed <= 6:
                    # Adds NW
                    surroundings.append([idy - 1, idx - 1])
                elif self.seed >= 7 and self.seed <= 9:
                    # Adds N
                    surroundings.append([idy - 1, idx])
            # Checks if there is a mountain to the East
            if self.board[idy][idx + 1] == self.mountainCode:
                if self.seed >= 1 and self.seed <= 3:
                    # Adds SW
                    surroundings.append([idy + 1, idx - 1])
                elif self.seed >= 4 and self.seed <= 6:
                    # Adds West
                    surroundings.append([idy, idx - 1])
                elif self.seed >= 7 and self.seed <= 9:
                    # Adds NW
                    surroundings.append([idy - 1, idx - 1])
            # Checks if there is a mountain to the North East
            if self.board[idy - 1][idx + 1] == self.mountainCode:
                if self.seed >= 1 and self.seed <= 3:
                    # Adds S
                    surroundings.append([idy + 1, idx])
                elif self.seed >= 4 and self.seed <= 6:
                    # Adds SW
                    surroundings.append([idy + 1, idx -1])
                elif self.seed >= 7 and self.seed <= 9:
                    # Adds West
                    surroundings.append([idy, idx - 1])
            # Checks if there is a mountain to the North
            if self.board[idy -1][idx] == self.mountainCode:
                if self.seed >= 1 and self.seed <= 3:
                    # Adds SE
                    surroundings.append([idy + 1, idx + 1])
                elif self.seed >= 4 and self.seed <= 6:
                    # Adds South
                    surroundings.append([idy + 1, idx])
                elif self.seed >= 7 and self.seed <= 9:
                    # Adds SW
                    surroundings.append([idy + 1, idx - 1])
            # Checks if there is a mountain to the NW
            if self.board[idy -1][idx - 1] == self.mountainCode:
                if self.seed >= 1 and self.seed <= 3:
                    # Adds East
                    surroundings.append([idy, idx + 1])
                elif self.seed >= 4 and self.seed <= 6:
                    # Adds SE
                    surroundings.append([idy + 1, idx + 1])
                elif self.seed >= 7 and self.seed <= 9:
                    # Adds South
                    surroundings.append([idy + 1, idx])
            # Checks if there is a mountain to the West
            if self.board[idy][idx - 1] == self.mountainCode:
                if self.seed >= 1 and self.seed <= 3:
                    # Adds NE
                    surroundings.append([idy - 1, idx + 1])
                elif self.seed >= 4 and self.seed <= 6:
                    # Adds E
                    surroundings.append([idy, idx + 1])
                elif self.seed >= 7 and self.seed <= 9:
                    # Adds SE
                    surroundings.append([idy + 1, idx + 1])
            if self.board[idy + 1][idx - 1] == self.mountainCode:
                if self.seed >= 1 and self.seed <= 3:
                    # Adds N
                    surroundings.append([idy -1, idx])
                elif self.seed >= 4 and self.seed <= 6:
                    # Adds NE
                    surroundings.append([idy - 1, idx + 1])
                elif self.seed >= 7 and self.seed <= 9:
                    # Adds East
                    surroundings.append([idy, idx + 1])

        for x in surroundings:
            if x[0] in self.allMountains:
                surroundings.remove(x)

        # Picks a random non-mountain from all the surroundings
        if len(surroundings) >= 1:
            self.mountainCoordinates = choice(surroundings)
            # Grabs the coordinates
            idy = self.mountainCoordinates[0]
            idx = self.mountainCoordinates[1] # Sets the new mountain
            self.board[idy][idx] = self.mountainCode
            self.mountainSeed -= 1

    def addSilver(self):
        # Random Placement of Silver Mines
        # We don't want many Silver Mines, they should be a harder resource to gather
        # We only want a few per map, so maybe 1 per 33 tiles rounded up seems good to me
        # If map size exceeds 50, it will add a random variance but there will always be one
        self.silverTiles = floor(self.mapSize / 500) + randint((floor(self.mapSize / -1000)), floor(self.mapSize / 1000))
        if self.silverTiles < 1:
            self.silverTiles = 1
        self.silverExist = False

        while self.silverExist == False:
            self.silverCoordinates = choice(self.allMountains)
            y = self.silverCoordinates[1]
            x = self.silverCoordinates[0]
            self.board[y][x] = self.silverCode
            self.silverTiles -= 1

            if self.silverTiles <= 0:
                self.silverExist = True

    def addQuarries(self):
        # Basically this will be the same as the Silver Mines
        self.stoneTiles = floor(self.mapSize / 500) + randint((floor(self.mapSize / -1000)), floor(self.mapSize / 1000))
        if self.stoneTiles < 1:
            self.stoneTiles = 1
        self.stoneExist = False

        while self.stoneExist == False:
            self.stoneCoordinates = choice(self.allMountains)
            y = self.stoneCoordinates[1]
            x = self.stoneCoordinates[0]
            self.board[y][x] = self.stoneCode
            self.stoneTiles -= 1

            if self.stoneTiles <= 0:
                self.stoneExist = True

    def addMetal(self):
        # Once again, just like the other two before it
        self.metalTiles = floor(self.mapSize / 500) + randint((floor(self.mapSize / -1000)), floor(self.mapSize / 1000))
        if self.metalTiles < 1:
            self.metalTiles = 1
        self.metalExist = False

        while self.metalExist == False:
            self.metalCoordiantes = choice(self.allMountains)
            y = self.metalCoordiantes[1]
            x = self.metalCoordiantes[0]
            self.board[y][x] = self.metalCode
            self.metalTiles -= 1

            if self.metalTiles <= 0:
                self.metalExist = True

    def addForest(self):
        # First iteration will seed a forest and the rest will randomly add adjacent or make a new seed
        self.board[randint(0, (len(self.board) - 1))][randint(0, (len(self.board) - 1))] = self.forestCode
        # Random placement of forests, 1/3 of tiles should be forests
        self.treeTiles = ceil(self.mapSize / 3) + randint(floor(self.mapSize / -10), floor(self.mapSize / 10))
        # While we need to add more treeTiles it will loop
        print('Tree Seeds', self.treeTiles)
        self.allForests = []
        while self.treeTiles >= 1:
            # Decides if the new tile will be seeded elsewhere or next to another forest
            self.seed = randint(0, 12)
            # Seed = 0 means that we seed a new forest
            if self.seed == 0:
                self.seedForest()
            # Anything else tells which direction to plant another forest
            else:
                self.allForests.clear()
                self.findFeature()
                self.placeForest()
        print('All Forests: ', len(self.allForests))

    def seedForest(self):
        # Picks random cordinate for new tree seed
        self.rand1 = randint(0, (len(self.board) - 1))
        self.rand2 = randint(0, (len(self.board) - 1))
        # Checks to make sure the tree seed in on a blank space
        if self.board[self.rand1][self.rand2] == self.plainsCode:
            # Places a F for Forest on the blank space
            self.board[self.rand1][self.rand2] = self.forestCode
            # If a forest has been placed, can reduce total treeTiles
            self.treeTiles -= 1
        return

    def placeForest(self):

        self.forestCoordinates = choice(self.allForests)
        idy = self.forestCoordinates[0]
        idx = self.forestCoordinates[1]
        # The seed decides the direction
        # 1 North, 2 East, 3 South, 4 West
        # makes sure that the row isn't the top most row as well
        if self.seed >= 1 and self.seed <= 3 and idy != 0:
            # Makes sure that the spot to be changed is blank
            if self.board[idy - 1][idx] == self.plainsCode:
                # Changes the blank spot to a forest
                self.board[idy - 1][idx] = self.forestCode
                # Drops the counter
                self.treeTiles -= 1
                # Logging
                #self.changed.append([idx, idy - 1, 'North', self.treeTiles])
                # Exits out of the function to prevent extra loops
                return
        # Slightly different, as the grid expands to the right, the furthest
        # area should be variable to accomodate any map size
        elif self.seed >= 4 and self.seed <= 6 and idx != (len(self.board[0]) - 1):
            if self.board[idy][idx + 1] == self.plainsCode:
                self.board[idy][idx + 1] = self.forestCode
                self.treeTiles -= 1
                #self.changed.append([idx + 1, idy, 'East', self.treeTiles])
        elif self.seed >= 7 and self.seed <= 9 and idy != (len(self.board) - 1):
            if self.board[idy + 1][idx] == self.plainsCode:
                self.board[idy + 1][idx] = self.forestCode
                self.treeTiles -= 1
                #self.changed.append([idx, idy + 1, 'South', self.treeTiles])
                return
        elif self.seed >= 10 and self.seed <= 12 and idx != 0:
            if self.board[idy][idx - 1] == self.plainsCode:
                self.board[idy][idx - 1] = self.forestCode
                self.treeTiles -= 1
                #self.changed.append([idx - 1, idy, 'West', self.treeTiles])
                return
        else:
            return

    def setBoard(self):

        """
        self.boardImage = Image.new('RGB', (self.castle.width * 2, self.castle.height))
        self.boardImage.paste(self.castle, (0, 0))
        self.boardImage.paste(self.plains, (self.castle.width, 0))
        self.boardImage.show()
        """
        self.boardImage = Image.new('RGB', (self.castle.width * self.boardSize, self.castle.height * self.boardSize))
        for idy, row in enumerate(self.boardASCII):
            for idx, column in enumerate(self.boardASCII):
                array = list(self.boardASCII[idy][idx])
                if array[0] == 'p':
                    self.boardImage.paste(self.plains, ((self.tileSize * idx),(self.tileSize *idy)))
                elif array[0] == 'f':
                    self.boardImage.paste(self.forest, ((self.tileSize * idx),(self.tileSize*idy)))
                elif array[0] == 's':
                    self.boardImage.paste(self.silverMine, ((self.tileSize * idx),(self.tileSize*idy)))
                elif array[0] == 'q':
                    self.boardImage.paste(self.stoneDeposit, ((self.tileSize * idx),(self.tileSize*idy)))
                elif array[0] == 'v':
                    self.boardImage.paste(self.mountain, ((self.tileSize * idx),(self.tileSize*idy)))
                elif array[0] == 'c':
                    self.boardImage.paste(self.castle, ((self.tileSize * idx), (self.tileSize * idy)))
                elif array[0] == 'm':
                    self.boardImage.paste(self.metal, ((self.tileSize * idx), (self.tileSize * idy)))

        #self.boardImage.show()
        self.boardImageTk = ImageTk.PhotoImage(self.boardImage)
        return self.boardImageTk

    def resizeImage(self, event, label):
        new_width = event.width
        new_height = event.height

        self.mapCopy = self.boardImage
        self.mapImage = self.boardImage.resize((new_width, new_height))

        self.board = ImageTk.PhotoImage(self.mapImage)
        label.configure(image = self.board)
