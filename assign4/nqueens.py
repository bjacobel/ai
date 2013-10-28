import getopt
import sys
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

    # given an array of queens, find out if this position is valid
    def isValid(self, queens):
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
                        return True
                        
        return False

    def __str__(self):
        return "Queen in row {}, column {}.".format(self.row, self.column)


def drawboard(numQueens):
    if numQueens > 25:
        print("Sorry, drawing the board for a problem of this size isn't practical.")
        return


    if numQueens < 10:
        qLabel = " Q"
    else:
        qLabel = "Q"
    hLineLen =  (7 * (numQueens)) + 1
    hLine = ""
    for i in xrange(0, hLineLen):
        hLine += "-"

    print(hLine)
    for i in xrange(0, numQueens*3):
        for j in xrange(0, numQueens):
            print("|     "),
        print("|")
        if i % 3 == 2:
            print(hLine)


def min_conflicts(queens, maxSteps):
    pass


def main():
    # default variables
    numQueens = 8
    maxSteps = 50

    # get commandline arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:")
    except getopt.GetoptError:
        print("Error in command line parameters. Continuing using 8 queens.")
    else:
        for opt, arg in opts:
            if opt == "-n":
                numQueens = arg
    
    #  create queens (really this is the constraint array, because the 
    #    constraint for each `queen` in `queens` is `queen.isValid(queens) == true`)
    queens = []
    for i in xrange(0, numQueens):
        queens.append(Queen(numQueens))

    for queen in queens:
        print(queen)
        if queen.isValid(queens):
            print("(That's a valid position!)")


if __name__ == "__main__":
    main()
