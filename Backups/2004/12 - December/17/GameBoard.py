class GameBoard:
    """The Squarez game board.

    A X by Y game board stored in a list as...
        square1, square2, ...squareN"""

    # A note on the structure of a board. The numbers are as follows:
    #   -1 is an invalid space (where pieces start out)
    #   0  is an empty space (nothing there)
    #   1  is an occupied space (something there)
    #   2  is a dead space (part of a square to be removed)
    #
    # Data stored as a three-list of (number, color, graphics)
    #   where number is a number as listed above, color is a number
    #   representing the color of the block, and grpahics is a space
    #   for the graphics to use (ostensibly for depth)
    #
    # The graphics element shows how high it is above the board in %

    def __init__(self, w = 16, h = 15, hx = 0, hy = 0):
        "Initaialize the board with a size of w by h and a magic square at hx, hy"
        self.width = w
        self.height = h
        self.board = []
        self.clearBoard()
        self.markMagicSquare(hx, hy);

    def markMagicSquare(self, x, y):
        for j in range(3):
            for i in range(3):
                self.setSquare(x + i, y + j, -1);

    def copyBoard(self, other):
        self.width = other.getWidth()
        self.height = other.getHeight()
        self.board = []

        for j in range(self.height):
            for i in range(self.width):
                self.setSquare(i, j, other.getSquare(i, j))

    def squareAt(self, x, y, mark):
        for j in range(3):
            for i in range(3):
                if self.getSquare(x, y) >= 1:
                    continue
                else:
                    return 0
        # Found a square, mark it if requested
        if mark:
            for j in range(3):
                for i in range(3):
                    self.setSquare(x, y, 2)
        return 1

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getList(self, x, y):
    	return self.board[x + y * self.width]

    def getSquare(self, x, y):
    	theList = self.getList(x, y)

    	return theList[0]

    def setSquare(self, x, y, state):
        theList = self.board[x + y * self.width]
        theList[0] = state
        self.board[x + y * self.width] = theList

    def setList(self, x, y, list):
    	self.board[x + y * self.width] = list

    def pieceCanFit(self, x, y, piece):
        "Check if the piece supplied will fit at the given position"

        # Note that there are some complications in this check.
        # Becuase of the fact a piece doesn't take up all of it's 3x3 grid,
        #   it's possible for a piece to be at a position such as -1. This
        #   complicates things. So we do some quick checks to make sure
        #   things are on the playing field, then we can do a very simple
        #   check if there are any collisions.

        # Return -1 = No collision, but in a magic square
        #         0 = No collision, no magic square
        #         1 = Collision

        # First we do some simple range checking

        if ((x < -1) or (y < -1)):
            return 0    # This isn't possible
        if ((x == self.width - 1) or (y == self.height - 1)):
            return 0    # Again, not possible

        # Now just a simple check

        magicCheck = 0

        for j in range(3):
            for i in range(3):
                if piece[i + j * 3]:
                    # There is a block here. Is it inside the grid?
                    if (((x + i) < 0) or ((x + i) >= self.width) or
                        ((y + j) < 0) or ((y + j) >= self.height)):
                        return 0    # A block would be outside of the field
                    # We're in the field, check for a collision
                    
                    squareValue = self.getSquare(x + i, y + j)

                    if (squareValue == -1):
                        magicCheck = 1
                        continue
                    elif (squareValue == 1):
                        return 1    # There was a collision, so it's not OK
                    else:
                        continue    # No collision, test next square
                else:
                    continue    # Nothing to collide, test next square

        if (magicCheck == 1):
            return -1
        else:
            return 0    # If we got here, there are no collisions so it's OK

    def placePiece(self, x, y, piece, color):
        for j in range(3):
            for i in range(3):
                if piece[i + j * 3]:
                    newList = [1, color, 100]
                    self.setList(x + i, y + j, newList)

    def setSize(self, w, h):
        self.__init__(w, h)

    def clearBoard(self):
        "Clears the board of pieces"
        
        squares = self.width * self.height
        
        for i in range(squares):
            newList = [0, 0, 0]
            self.board.insert(i, newList)
