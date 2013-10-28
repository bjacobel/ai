import getopt
import sys
from random import randint

class Queen:
    def __init__(self, boardSize):
        self.row = randint(0, boardSize-1)
        self.column = randint(0, boardSize-1)
        self.boardSize = boardSize

    def moveRow(newRow):
        self.row = newRow

    def moveColumn(newColumn):
        self.column = newColumn

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
            
            # check diagonals (hard)
            downDiagRow = upDiagRow = self.row
            downDiagColumn = upDiagColumn = self.column

            # trace each diagonal the row is in back the the left side of the board
            # trace the downward-slanting diagonal up as far as it will go and the
            #   upward-slanting diagonal down as far as it will go
            while downDiagRow > 0 and downDiagColumn > 0:
                downDiagRow -= 1
                downDiagColumn -= 1
            while upDiagRow < self.boardSize - 1 and upDiagColumn > 0:
                upDiagRow += 1
                upDiagColumn -= 1

            # follow upDiag northeast until it runs out, check if there's people there at each step
            while upDiagRow > 0 and upDiagColumn < self.boardSize - 1:
                upDiagRow -= 1
                upDiagColumn += 1
                for queen in queens:
                    if queen.row == upDiagRow and queen.column == upDiagColumn:
                        return False

            # follow downDiag southeast until it runs out, check if there's people there at each step
            while downDiagRow < self.boardSize - 1 and downDiagColumn < self.boardSize - 1:
                downDiagRow += 1
                downDiagColumn += 1
                for queen in queens:
                    if queen.row == downDiagRow and queen.column == downDiagColumn:
                        return False

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
