from random import randint

class Queen:
    def __init__(self, boardSize):
        self.row = randint(0, boardSize-1)
        self.column = randint(0, boardSize-1)
        self.boardSize = boardSize

    def moveRow(self, newRow):
        self.row = newRow

    def moveColumn(self, newColumn):
        self.column = newColumn
   
    # returns the number of the square which, if a diagonal were drawn northeast
    # from this square to one of the numbered squares, the diagonal would intercept.
    # "numbered squares" are the squares on the east and north sides of the grid.
    # they are numbered clockwise from southeast.
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

    # returns the number of the square which, if a diagonal were drawn southeast
    # from this square to one of the numbered squares, the diagonal would intercept.
    # "numbered squares" are the squares on the east and south sides of the grid.
    # they are numbered counter-clockwise from northeast.
    # "Up diagonals" are so named because they have a slope of positive 1.
    def baseUpDiagonal(self):
        upDiagRow = self.row
        upDiagColumn = self.column
        while upDiagRow != self.boardSize - 1 and upDiagColumn != 0:
            upDiagRow += 1
            upDiagColumn -= 1
        if upDiagColumn == 0:
            return self.boardSize - 1 - upDiagRow
        else: 
            return (self.boardSize - 1 - upDiagRow) + upDiagColumn

    # given an array of queens, find out if this position is valid and how many conficts it has
    def validator(self, queens):
        numConflicts = 0

        usedRows = []
        usedColumns = []
        for queen in queens:
            usedRows.append(queen.row)
            usedColumns.append(queen.column)

        # Check horizontal and vertical: there sould be exactly one instance of this row and column in queens
        # This is easy to do, so we'll do it before the diagonal checking    
        if usedRows.count(self.row) == 1 and usedColumns.count(self.column) == 1:

            # "up diagonals" go from SW to NE, "down diagonals" go from NW to SE
            # there are boardSize*2-1 of each
            usedUpDiagonals = []
            usedDownDiagonals = []
            for queen in queens:
                usedUpDiagonals.append(queen.baseUpDiagonal())
                usedDownDiagonals.append(queen.baseDownDiagonal())

            for i in xrange(0, self.boardSize*2-1):
                for j in xrange(0, self.boardSize*2-1):
                    if usedUpDiagonals.count(i) == 1 and usedDownDiagonals.count(j) == 1:
                        return True, numConflicts

            # find the number of conflicts in diagonals
            numConflicts += usedUpDiagonals.count(self.baseUpDiagonal())
            numConflicts += usedDownDiagonals.count(self.baseDownDiagonal())

        # find the number of conflics in rows and columns
        numConflicts += usedRows.count(self.row)
        numConflicts += usedColumns.count(self.column)
        
        return False, numConflicts

    # interfaces for finding just the truth value or the number of conflicts, respectively
    def isValid(self, queens):
        valid, numConflicts = self.validator(queens)
        return valid

    def numConflicts(self, queens):
        valid, numConflicts = self.validator(queens)
        return numConflicts

    def __str__(self):
        return "Queen in row {}, column {}.".format(self.row, self.column)