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
        if usedRows.count(self.row) == 1 and usedColumns.count(self.column) == 1:
            # check diagonals (hard)
            diagRow = self.row
            diagColumn = self.column
            while(diagRow <= self.boardSize-1 and diagColumn <= self.boardSize-1):
                diagRow++
                diagColumn++
                for queen in queens:
                    if(queen.row == diagRow and queen.column == diagColumn)
                        return False
            while(diagRow >= 0 and diagColumn >= 0):
                diagRow--
                diagColumn--
                for queen in queens:
                    if(queen.row == diagRow and queen.column == diagColumn)
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
        qLabel += " Q"
    else:
        qLabel = "Q"
    hLineLen =  (7 * (numQueens)) + 1
    hLine = ""
    for i in xrange(0, hLineLen):
        hLine += "-"

    print hLine
    for i in xrange(0, numQueens*3):
        for j in xrange(0, numQueens):
            print("|     "),
        print("|")
        if i % 3 == 2:
            print hLine


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

    # draw the solved board
    drawboard(numQueens)

    for queen in queens:
        print queen
        if queen.isValid(queens):
            print("(That's a valid position!)")


if __name__ == "__main__":
    main()
