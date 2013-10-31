from random import randint

class Queen:
    def __init__(self, column, boardsize):
        self.column = column
        self.boardSize = boardsize

        # Original code: row is always 0
        # self.row = 0

        # Improved code: rows are selected via a devisation of mine own which should give fairly low initial conflicts
        countDown = countUp = 0
        if column % 2 == 0:
            self.row = countDown
            countDown += 1
        else:
            self.row = self.boardSize - 1 - countUp
            countUp += 1

        # See what I'm doing? Pieces are distributed alternatingly from the top and bottom, incrementing towards the middle one at a time from each side.
        # This sould minimize diagonal conflicts initially, and completely eliminate initial row conflicts


    def move(self, newRow):
        self.row = newRow
   
    # returns the number of the square which, if a diagonal were drawn up and left
    # from this square to one of the numbered squares, the diagonal would intercept.
    # "numbered squares" are the squares on the left and top sides of the grid.
    # they are numbered clockwise from bottom left, starting at 0.
    # "Down diagonals" are so named because they have a slope of negative 1.
    def baseDownDiagonal(self):
        downDiagRow = self.row
        downDiagColumn = self.column
        while downDiagRow != 0 and downDiagColumn != 0:
            downDiagRow -= 1
            downDiagColumn -= 1
        if downDiagColumn == 0:
            return self.boardSize - 1 - downDiagRow
        else: 
            return (self.boardSize - 1 - downDiagRow) + downDiagColumn

    # returns the number of the square which, if a diagonal were drawn down and left
    # from this square to one of the numbered squares, the diagonal would intercept.
    # "numbered squares" are the squares on the left and bottom sides of the grid.
    # they are numbered counter-clockwise from top left, starting at 0.
    # "Up diagonals" are so named because they have a slope of positive 1.
    def baseUpDiagonal(self):
        upDiagRow = self.row
        upDiagColumn = self.column
        while upDiagRow != self.boardSize - 1 and upDiagColumn != 0:
            upDiagRow += 1
            upDiagColumn -= 1
        if upDiagColumn == 0:
            return upDiagRow
        else: 
            return upDiagRow + upDiagColumn

    # given an array of queens, find out if this position is valid and how many conficts it has
    def validator(self, queens):
        straightConflicts = diagonalConflicts = 0
        straightLinesOK = False
        diagonalLinesOK = False

        ## CHECK HORIZONTAL/VERTICAL ##
        # there sould be exactly one instance of this row in queens
        usedRows = []
        for queen in queens:
            usedRows.append(queen.row)
 
        if usedRows.count(self.row) == 1:
            straightLinesOK = True
        else:
            straightConflicts += usedRows.count(self.row)-1


        ## CHECK DIAGONAL ##
        # "up diagonals" go from SW to NE, "down diagonals" go from NW to SE
        # there are boardSize*2-1 of each
        usedUpDiagonals = []
        usedDownDiagonals = []
        for queen in queens:
            usedUpDiagonals.append(queen.baseUpDiagonal())
            usedDownDiagonals.append(queen.baseDownDiagonal())

        if usedUpDiagonals.count(self.baseUpDiagonal()) == 1 and usedDownDiagonals.count(self.baseDownDiagonal()) == 1:
            diagonalLinesOK = True
        else:
            diagonalConflicts += usedUpDiagonals.count(self.baseUpDiagonal())-1
            diagonalConflicts += usedDownDiagonals.count(self.baseDownDiagonal())-1

        if diagonalLinesOK and straightLinesOK:
            return True, 0
        else:
            return False, straightConflicts + diagonalConflicts

    # interfaces for finding just the truth value or the number of conflicts, respectively
    def isValid(self, queens):
        valid, numConflicts = self.validator(queens)
        return valid

    def numConflicts(self, queens):
        valid, numConflicts = self.validator(queens)
        return numConflicts

    def __str__(self):
        return "Queen in row {}, column {}.".format(self.row, self.column)