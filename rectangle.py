class Rectangle:
    def __init__(self, x1, y1, x2, y2,
                tType, worker,
                resource, rProduction,
                armySize, player):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.tType = tType
        self.worker = worker
        self.resource = resource
        self.rProduction = rProduction
        self.armySize = armySize
        self.player = player

    def contains(self, newx, newy):
        # Will return true if the given point (newx, newy) 
        # is within the rectangle or it will return false 
        # otherwise
        return (self.x1 <= newx <= self.x2) and (self.y1 <= newy <= self.y2)
    def report(self):
        print('(%s, %s), (%s, %s)' % (self.x1, self.y1, self.x2, self.y2))
        print('tType: %s\nplayer: %d' % (self.tType, self.player))
