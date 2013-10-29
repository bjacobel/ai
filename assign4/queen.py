from random import randint

class Queen:
    def __init__(self, boardSize):
        self.row = randint(0, boardSize-1)
        self.column = randint(0, boardSize-1)
        self.boardSize = boardSize

    def move(self, newRow, newColumn):
        self.row = newRow
        self.column = newColumn
   
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
        numConflicts = 0
        straightLinesOK = False
        diagonalLinesOK = False

        ## CHECK HORIZONTAL/VERTICAL ##
        # there sould be exactly one instance of this row and column in queens
        usedRows = []
        usedColumns = []
        for queen in queens:
            usedRows.append(queen.row)
            usedColumns.append(queen.column)
 
        if usedRows.count(self.row) == 1 and usedColumns.count(self.column) == 1:
            straightLinesOK = True
        else:
            # find the number of conflicts in rows and columns
            numConflicts += usedRows.count(self.row)-1
            numConflicts += usedColumns.count(self.column)-1


        ## CHECK DIAGONAL ##
        # "up diagonals" go from SW to NE, "down diagonals" go from NW to SE
        # there are boardSize*2-1 of each
        usedUpDiagonals = []
        usedDownDiagonals = []
        for queen in queens:
            usedUpDiagonals.append(queen.baseUpDiagonal())
            usedDownDiagonals.append(queen.baseDownDiagonal())

        print(usedUpDiagonals)
        print(usedDownDiagonals)

        if usedUpDiagonals.count(self.baseUpDiagonal()) == 1 and usedDownDiagonals.count(self.baseDownDiagonal()) == 1:
            diagonalLinesOK = True
        else:
            print("{} queens in up diagonal {}".format(usedUpDiagonals.count(self.baseUpDiagonal()), self.baseUpDiagonal()))
            print("{} queens in down diagonal {}".format(usedDownDiagonals.count(self.baseDownDiagonal()), self.baseDownDiagonal()))
            numConflicts += usedUpDiagonals.count(self.baseUpDiagonal())-1
            numConflicts += usedDownDiagonals.count(self.baseDownDiagonal())-1

        if diagonalLinesOK and straightLinesOK:
            return True, 0
        else:
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