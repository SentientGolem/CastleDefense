class Player():
    def __init__(self, ID, silver, metal,
                 stone, wood, food, population):
        self.ID = ID
        self.silver = silver
        self.metal = metal
        self.stone = stone
        self.wood = wood
        self.food = food
        self.population = population

        self.claims = []

    def can_Claim(self, adjacent):
        # If there are no current claims, run through
        # the preliminary claims
        if len(self.claims) == 0:
            return 'castle'
        # Needs to check if your claims exceeds your pop
        # and if your new claim is adjacent to another
        elif len(self.claims) - 9 < self.population:
            # Checks if any of the rectangles adjacent to the
            # selected rectangle are already claimed
            for rectangle in adjacent:
                if rectangle in self.claims:
                     return True
            # If it can't find any, it returns false
            return False
        else:
            return False

    def claim(self, rectangle, board, x, y):
        # We need to assign the correct rectangle but the grid
        # is changed every time a tile is pressed so every time 
        # a tile is changed or resized, the rectangles change
        if rectangle not in self.claims:
            self.claims.append(rectangle)
            array = list(board[x-1][y-1])
            array[3] = str(self.ID)
            board[x-1][y-1] = ''.join(array)
            print(board[x-1][y-1])
            print(self.claims)
        else:
            print('Already claimed!')

