# A Game About Building up a Castle to Defend from Threats
# By Nicholas Eguizabal
from tkinter import Tk, Frame, Label, Button, Canvas, Toplevel, Text, DISABLED, NORMAL
# This calls in our map generator class
from mapGen import mapGen
from rectangle import Rectangle
from math import ceil
from sys import platform
from player import Player

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title('Defend the Castle!')

        # This makes a mapGen object, which generate a map
        # The map itself is under the board attribute 
        # Which is an ImageTk type
        self.pixMap = mapGen(self.master)
        # Player(self, ID, silver, metal, stone, wood, food, population)
        self.player = Player(1, 0, 0, 0, 0, 0 , 1)

        self.make_Container()
        self.make_Label()
        self.make_Canvas()
        self.make_Button()
        self.make_Grid()
        self.make_Descriptor()

        master.bind('<Escape>', self.quit)
        master.bind('<Right>', lambda event: self.move(event, self.pixMap.tileSize, 0))
        master.bind('<Left>', lambda event: self.move(event, (-1*self.pixMap.tileSize), 0))
        master.bind('<Up>', lambda event: self.move(event, 0, (-1* self.pixMap.tileSize)))
        master.bind('<Down>', lambda event: self.move(event, 0, self.pixMap.tileSize))
        self.bgCanvas.bind('<Button-1>', self.button_click)
        self.bgCanvas.bind('<Motion>', self.toolTip)
        master.bind('<Tab>', self.toggleText)
        master.bind('<greater>', lambda event: self.zoom(event, 'in'))
        master.bind('<less>', lambda event: self.zoom(event, 'out'))
        if platform.startswith('linux'):
            master.bind('<Button-4>', lambda event: self.zoom(event, 'in'))
            master.bind('<Button-5>', lambda event: self.zoom(event, 'out'))
        elif playform.startswith('win32') or sys.platform.startswith('cygwin'):
            master.bind('<MouseWheel>', self.windowWheel)

    def windowWheel(self, event):
        pass

    def endTurn(self):
        # This function is to run through all the player's end turns
        self.endPlayer(self.player)

    def endPlayer(self, player):
        # This is a generalized function for any player to run through their turn things
        print(player.claims)
        for claim in player.claims:
            print('tType: %s\nResource: %s\nResources Produced: %d' % (claim.tType, claim.resource, claim.rProduction))
            if claim.resource == 'Wood':
                self.Player.wood += claim.rProduction
                print('Added wood')
            elif claim.resource == 'Stone':
                self.player.wood += claim.rProduction
                print('Added Stone')
            elif claim.resource == 'Food':
                self.player.food += claim.rProduction
                print('Added wood')
            elif claim.resource == 'Ore':
                self.player.metal += claim.rProduction
                print('Added metal')
            elif claim.resource == 'Silver':
                self.player.silver += claim.rProduction
                print('Added silver')
            print(claim.resource)
        self.update_Labels()

    def button_click(self, event):
        # Looks at the top left corner of the view, the 'relative 0,0'
        # and finds out where they are on the entire image
        (cx0, cy0) = (self.bgCanvas.canvasx(0), self.bgCanvas.canvasy(0))
        # Adds the 'relative 0,0' of the canvas and adds them with the 
        # relative location of the cursor to get the actual location 
        # of the picture
        self.xClick = cx0 + event.x
        self.yClick = cy0 + event.y
        # Testing code to ensure the clicked location is accurate
        print('{}, {})'.format(self.xClick, self.yClick))
        # Begins iteration through the entire grid looking for the 
        # matching coordinates to a specific object
        for name, rectangles in self.grid.items():
            if rectangles.contains(self.xClick, self.yClick):
                # Testing code to tell which rectangle it is
                print('This worked! %s' % name)
                # Testing code to tell the exact coordinates this 
                # rectangle object keeps track of
                rectangles.report()
                # This changes the larger of the two sets of coordinates
                # back into their specific grid location as the coordinates
                # should always be the tile size * the index
                self.x = int((rectangles.y1 / self.pixMap.tileSize) + 1)
                self.y = int((rectangles.x1 / self.pixMap.tileSize) + 1)
                # Calls the change that should happen
                # Checks if claiming is currently on
                if self.claim == True:
                    if self.player.can_Claim() == 'castle':
                        self.changeTile(self.x, self.y, 'castle')
                        self.player.claim(rectangles, self.pixMap.boardASCII, self.x, self.y)
                        self.name = '(%s, %s)' % (self.x - 1, self.y - 2)
                        self.player.claim(self.grid[self.name], self.pixMap.boardASCII, self.x - 1, self.y - 2)
                        self.name = '(%s, %s)' % (self.x - 1, self.y)
                        self.player.claim(self.grid[self.name], self.pixMap.boardASCII, self.x - 1, self.y)
                        self.name = '(%s, %s)' % (self.x - 2, self.y - 1)
                        self.player.claim(self.grid[self.name], self.pixMap.boardASCII, self.x - 2, self.y - 1)
                        self.name = '(%s, %s)' % (self.x, self.y - 1)
                        self.player.claim(self.grid[self.name], self.pixMap.boardASCII, self.x, self.y - 1)
                    elif self.player.can_Claim() == True:
                        self.player.claim(rectangles, self.pixMap.boardASCII, self.x, self.y)
                    elif self.player.can_Claim() == False:
                        print('Cannot claim\nPopulation: %d\nClaims: %d' % (self.player.population, len(self.player.claims)))

                    self.update_Grid()
                else:
                    print('Claiming is off!')
                    # Returns the function so that multiple rectangles can't be clicked
                return

    def changeTile(self, x, y, newTile):
        # Changes the ASCII board that the picture is based on
        if newTile == 'castle':
            tile = self.pixMap.castle
            code = self.pixMap.castleCode
        elif newTile == 'plains':
            tile = self.pixMap.plains
            code = self.pixMap.plainsCode
        self.pixMap.boardASCII[x - 1][y - 1] = code
        # Remakes the picture with the new ASCII board
        self.pixMap.board = self.pixMap.setBoard()
        # Deletes the old map from the canvas
        self.bgCanvas.delete('map')
        # Creates the new map on the canvas
        self.bgCanvasImage = self.bgCanvas.create_image(0, 0, image = self.pixMap.board, anchor = 'nw', tags = 'map')

    def toolTip(self, event):
        # Finds the 'relative 0,0'
        (cx0, cy0) = (self.bgCanvas.canvasx(0), self.bgCanvas.canvasy(0))
        # Creates the true location of the cursor
        self.xClick = cx0 + event.x
        self.yClick = cy0 + event.y
        # Begins iteration through the rectangles objects
        for name, rectangles in self.grid.items():
            if rectangles.contains(self.xClick, self.yClick):
                self.text.config(state = NORMAL)
                self.text.delete('1.0', 'end')
                self.text.insert('end', '%s\nWorking: %s\nResource: %s\nProduces: %d\n Army: %d\nCoordinates: (%d, %d)\nPlayer: %d' %
                                 (rectangles.tType, rectangles.worker,
                                  rectangles.resource, rectangles.rProduction,
                                 rectangles.armySize, (rectangles.x2 / self.pixMap.tileSize) - 1,
                                  (rectangles.y2 / self.pixMap.tileSize) - 1, rectangles.player))
                self.text.config(state = DISABLED)

    def toggleText(self, event):
        # Checks to see if the text box is visible
        if self.text.winfo_ismapped():
            # If it is, hide it away
            self.text.place_forget()
            self.claimButton.place_forget()
            self.turnButton.place_forget()
        else:
            # If it isn't, we need to bring it back
            self.text.place(relx = .85, rely = .75)
            self.turnButton.place(relx = .15, rely = .965, relheight = .035, relwidth = .15)
            self.claimButton.place(relx = 0, rely = .965, relheight = .035, relwidth = .15)

    def move(self, event, deltax, deltay):
        # Changes the x-coordinates of the top-left point of the canvas
        # This moves it by pixels
        self.bgCanvas.xview('scroll', int(deltax), 'units')
        # Changes the y-coordinates of the top-left point of the canvas
        self.bgCanvas.yview('scroll', int(deltay), 'units')

    def zoom(self, event, direction):
        # Keeps a record of the old tileSize for comparison
        self.oldSize = self.pixMap.tileSize
        # Checks in we're zooming in and makes sure it doesn't get too big
        if direction == 'in' and self.pixMap.tileSize < 40:
            # Increases the size of all the tiles by 5x5
            self.pixMap.tileSize += 10
            # Calls the function to recreate the map and recenter it
            self.recreate(event)
        # Checks if we're zooming out and makes sure we don't get down to 0x0
        elif direction == 'out' and self.pixMap.tileSize > 10:
            # Decreases the size of all the tiles by 5x5
            self.pixMap.tileSize -= 10
            # Calls the function to recreate the map and recenter it
            self.recreate(event)

    def recreate(self, event):
        # Finds the 'relative 0,0' of the canvas
        (cx0, cy0) = (self.bgCanvas.canvasx(0), self.bgCanvas.canvasy(0))
        # Calculates the actual point of the cursor on the map
        (xClick0, yClick0) = (event.x + cx0, event.y + cy0)
        # This gets rid of the old map
        self.bgCanvas.delete('map')
        # This resizes all the pictures to the new tile size
        self.pixMap.setPictures()
        # This recreates the image with the new tile size
        self.pixMap.board = self.pixMap.setBoard()
        # This resizes the canvas size to accomodate the bigger picture
        self.bgCanvas.configure(scrollregion = (0, 0, self.pixMap.board.width(),
                                                 self.pixMap.board.height()))
        # This recreates the canvas images
        self.bgCanvasImage = self.bgCanvas.create_image(0, 0, image = self.pixMap.board, anchor = 'nw', tags = 'map')
        # This recreates the grid according to the new size of the picture
        self.make_Grid()
        # This tells us how much the image has been zoomed in or out
        zoomFactor = self.pixMap.tileSize / self.oldSize
        # This tells us how big the window is
        # The canvas should be about twice the size of the window
        x_offset = (self.master.winfo_reqwidth() / 2)
        y_offset = (self.master.winfo_reqheight() / 2)
        # This takes the old location of the mouse, multiplies it by the zoomFactor
        # to tell us where the same old location will be on the new canvas.
        # The 'moveto' function takes a relative position between 0~1 to place the 
        # upper left corner that far into the full map.
        # Then it gets divided by the full size of the map to get the fraction
        mouseX = ((zoomFactor * xClick0) - x_offset) / self.pixMap.board.width()
        mouseY = ((zoomFactor * yClick0) - y_offset) / self.pixMap.board.height()
        # We input the relative position and it moves the view
        # This typically means putting the zoomed in tile at the center of the 
        # screen as best it can when edges are concerned.
        self.bgCanvas.xview('moveto', mouseX)
        self.bgCanvas.yview('moveto', mouseY)

    def make_Container(self):
        # Creates a frame for all the widgets in the application
        self.container = Frame(self.master)
        self.container.grid(row = 0, column = 0, sticky = 'NESW')
        # This will make the application scale with the window
        # in both width and height
        self.master.grid_rowconfigure(0, weight = 1)
        self.master.grid_columnconfigure(0, weight = 1)
        # This will make the first 4 columns and rows equally scale with the window
        self.container.grid_columnconfigure((0, 1, 2, 3), weight = 1, uniform = 'equal')
        self.container.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight = 1, uniform = 'equal')

    def make_Descriptor(self):
        # This creates a text box
        self.text = Text(height = 10, width = 15, bg = '#1318a1', fg = 'white',
                        bd = 0, font = ("Noto Sans", 12), wrap = 'word')
        # This makes sure the text box floats in the bottom right of the window
        # regardless of window size
        self.text.place(relx = .85, rely = .75)
        # This makes sure that the text box can't be interacted with by anyone else
        # We just want it to hold text for us
        self.text.config(state = DISABLED)

    def make_Label(self):
        self.silverLabel = Label(self.container, text = 'Silver: %d' % self.player.silver)
        self.silverLabel.grid(row = 0, column = 0, sticky = 'NESW')
        self.stoneLabel = Label(self.container, text = 'Stone: %d' % self.player.stone)
        self.stoneLabel.grid(row = 0, column = 1, sticky = 'NESW')
        self.foodLabel = Label(self.container, text = 'Food: %d' % self.player.food)
        self.foodLabel.grid(row = 0, column = 2, sticky = 'NESW')
        self.populationLabel = Label(self.container, text = 'Population: %d' % self.player.population)
        self.populationLabel.grid(row = 0, column = 3, sticky = 'NESW')
        self.metalLabel = Label(self.container, text = 'Metal: %d' % self.player.metal)
        self.metalLabel.grid(row = 0, column = 4, sticky = 'NESW')

    def update_Labels(self):
        self.silverLabel.config(text = 'Silver: %d' % self.player.silver)
        self.stoneLabel.config(text = 'Stone: %d' % self.player.stone)
        self.foodLabel.config(text = 'Food: %d' % self.player.food)
        self.populationLabel.config(text = 'Population: %d' % self.player.population)
        self.metalLabel.config(text = 'Metal: %d' % self.player.metal)
        print('Labels updated!')

    def make_Button(self):
        self.claim = False
        self.claimButton = Button(height = 1, width = 15, bg = '#1318a1', fg = 'white',
                                  bd = 0, font = ("Noto Sans", 12), text = 'Claim',
                                  command = self.claiming)
        self.claimButton.place(relx = 0, rely = .965, relheight = .035, relwidth = .15)

        self.turnButton = Button(height = 1, width = 15, bg = '#1318a1', fg = 'white',
                                 bd = 0, font = ("Noto Sans", 12), text = 'End Turn',
                                command = self.endTurn)
        self.turnButton.place(relx = .15, rely = .965, relheight = .035, relwidth = .15)

        self.workedButton = Button (height = 1, width = 15, bg = '#1318a1', fg = 'white',
                                    bd = 0, font = ('Noto Sans', 12), text = 'Assign Workers')
        self.workedButton.place(relx = .30, rely = .965, relheight = .035, relwidth = .15)

    def claiming(self):
        if self.claim == True:
            self.claim = False
        elif self.claim == False:
            self.claim = True

    def make_Grid(self):

        # This grid should be made dynamically so it will iterate through until
        # it has enough rectangles to fill up the entire canvas. 
        # These aren't a Tkinter object, these are closer to variables holding 
        # onto the coordinates for different areas.
        self.grid = {}
        self.grid.clear()
        # This creates a loop that is one larger than the boardsize
        # And it stands in for the y coordinate
        for y in range(self.pixMap.boardSize + 1):
            # This creates another loop, while y is 0, x will iterate through 100
            # And it stands in for the x coordinate
            for x in range(self.pixMap.boardSize + 1):
                self.name = '(%s, %s)' % (x-1, y-1)
                # Creates the far left bound of the rectangle
                x1 = (y - 1) * self.pixMap.tileSize
                # Creates the upper bound of the rectangle
                y1 = (x - 1) * self.pixMap.tileSize
                # Creates the rightmost bound of the rectangle
                x2 = y * self.pixMap.tileSize
                # Creates the bottom bound of the rectangle
                y2 = x * self.pixMap.tileSize
                # Creates an array that breaks apart the code for the tile
                array = list(self.pixMap.boardASCII[x-1][y-1])
                array[1] = int(array[1])
                array[2] = int(array[2])
                array[3] = int(array[3])
                if array[0]  == 'f':
                    self.grid[self.name] = Rectangle(x1, y1, x2, y2,
                                                     'Forest', False,
                                                     'Wood', array[1], array[2],
                                                    array[3])
                elif array[0]  == 'p':
                    self.grid[self.name] = Rectangle(x1, y1, x2, y2,
                                                     'Plains', False,
                                                     'Food', array[1], array[2],
                                                    array[3])
                elif array[0] == 's':
                    self.grid[self.name] = Rectangle(x1, y1, x2, y2,
                                                     'Silver Deposit', False,
                                                     'Silver', array[1], array[2],
                                                    array[3])
                elif array[0] == 'q':
                    self.grid[self.name] = Rectangle(x1, y1, x2, y2,
                                                     'Stone Deposit', False,
                                                     'Stone', array[1], array[2],
                                                    array[3])
                elif array[0] == 'v':
                    self.grid[self.name] = Rectangle(x1, y1, x2, y2,
                                                     'Mountain', False,
                                                     'None', array[1], array[2],
                                                    array[3])
                elif array[0] == 'c':
                    self.grid[self.name] = Rectangle(x1, y1, x2, y2,
                                                     'Castle', False,
                                                     'Food', array[1], array[2],
                                                     array[3])
                elif array[0] == 'm':
                    self.grid[self.name] = Rectangle(x1, y1, x2, y2,
                                                     'Metal Deposit', False,
                                                     'Ore', array[1], array[2],
                                                     array[3])

    def update_Grid(self):
        for y in range(self.pixMap.boardSize + 1):
            for x in range(self.pixMap.boardSize + 1):
                self.name = '(%s, %s)' % (x - 1, y - 1)
                x1 = (y - 1) * self.pixMap.tileSize
                y1 = (x - 1) * self.pixMap.tileSize
                x2 = y * self.pixMap.tileSize
                y2 = x * self.pixMap.tileSize
                array = list(self.pixMap.boardASCII[x-1][y-1])
                array[1] = int(array[1])
                array[2] = int(array[2])
                array[3] = int(array[3])
                self.grid[self.name].x1  = x1
                self.grid[self.name].y1 = y1
                self.grid[self.name].x2 = x2
                self.grid[self.name].y2 = y2
                self.grid[self.name].rProduction = array[1] + 1
                self.grid[self.name].armySize = array[2]
                self.grid[self.name].player = array[3]
                if array[0] == 'f':
                    self.grid[self.name].tType = 'Forest'
                elif array[0] == 'p':
                    self.grid[self.name].tType = 'Plains'
                elif array[0] == 's':
                    self.grid[self.name].tType = 'Silver Deposit'
                elif array[0] == 'q':
                    self.grid[self.name].tType = 'Stone'
                elif array[0] == 'v':
                    self.grid[self.name].tType = 'Mountain'
                elif array[0] == 'c':
                    self.grid[self.name].tType = 'Castle'
                elif array[0] == 'm':
                    self.grid[self.name].tType = 'Metal Deposit'

    def make_Canvas(self):
        self.bgCanvas = Canvas(self.container, background = 'black', width = 1000, height = 1000)
        self.bgCanvas.configure(scrollregion = (0, 0, self.pixMap.board.width(),
                                               self.pixMap.board.height()),
                                borderwidth = 0, xscrollincrement = 1,
                                yscrollincrement = 1)
        self.bgCanvasImage = self.bgCanvas.create_image(0, 0, image = self.pixMap.board, anchor = 'nw', tags = 'map')
        self.bgCanvas.grid(row = 1, column = 0, rowspan = 6, columnspan = 5, sticky = 'NESW')

    def quit(self, event):
        self.master.destroy()


root = Tk()
main = Main(root)
root.mainloop()
