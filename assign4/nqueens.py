import getopt
import sys
from random import randint
from queen import Queen

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


# method separate from __main()__ so this can be imported & called from a tester class
def run(numQueens, maxSteps):
    #  create queens (really this is the constraint array, because the 
    #    constraint for each `queen` in `queens` is `queen.isValid(queens) == true`)
    queens = []
    for i in xrange(0, numQueens):
        queens.append(Queen(numQueens))

    for i in xrange(0, maxSteps):
        # if all queens are in valid positions
        if all(queen.isValid(queens) for queen in queens):
            print("Solution found:")
            drawboard(numQueens)
            return

        # randomly find a queen in an invalid position
        while True:  # this is awkward, I wish Python had a do-while
            unsatisfier = queens[randint(0, numQueens-1)]
            if not unsatisfier.isValid(queens):
                break

        print unsatisfier.numConflicts(queens)

    print ("No solution found. Sorry.")
          

def main():
    # default variables
    numQueens = 8
    maxSteps = 50

    # get commandline arguments (if running interactively)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:")
    except getopt.GetoptError:
        print("Error in command line parameters. Continuing using {} queens.".format(numQueens))
    else:
        for opt, arg in opts:
            if opt == "-n":
                numQueens = arg

    run(numQueens, maxSteps)

if __name__ == "__main__":
    main()
