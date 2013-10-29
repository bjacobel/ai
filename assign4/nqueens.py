import getopt
import sys
from random import randint, choice
from queen import Queen

def drawboard(queens):
    numQueens = len(queens)

    if numQueens > 25:
        print("Solution found.")
        return
    
    hLineLen =  (7 * (numQueens)) + 1
    hLine = ""

    for i in range(0, hLineLen):
        hLine += "-"

    print(hLine)
    for row in range(0, numQueens):
        for column in range(0, numQueens):
            print("|     "),
        print("|")
        for column in range(0, numQueens):
            hasQueen = False
            for queen in queens:
                if queen.row == row and queen.column == column:
                    if queens.index(queen) < 10:
                        label = " Q"+str(queens.index(queen))
                    else:
                        label = "Q"+str(queens.index(queen))
                    print("| {} ".format(label)),
                    hasQueen = True
            if not hasQueen:
                print("|     "),
        print("|")
        for column in range(0, numQueens):
            print("|     "),        
        print("|")
        print(hLine)


# method separate from __main()__ so this can be imported & called from a tester class
def run(numQueens, maxSteps):
    #  create queens (really this is the constraint array, because the 
    #    constraint for each `queen` in `queens` is `queen.isValid(queens) == true`)
    queens = []
    for i in range(0, numQueens):
        queens.append(Queen(numQueens))

    for i in range(0, maxSteps):
        totalConflicts = 0
        for queen in queens:
            totalConflicts += queen.numConflicts(queens)
        # if all queens are in valid positions
        if all(queen.isValid(queens) for queen in queens):
            drawboard(queens)
            return True

        # randomly find a queen in an invalid position
        while True:  # this is awkward, I wish Python had a do-while
            unsatisfier = choice(queens)
            if not unsatisfier.isValid(queens):
                break

        # try new locations for unsatisfier, find a set of candidate locations that has the same or less conflicts
        bestNumConflicts = unsatisfier.numConflicts(queens)
        candidateNewLocs = []
        for tryrow in range(0, numQueens-1):
            for trycolumn in range(0, numQueens-1):
                if (tryrow, trycolumn) != (unsatisfier.row, unsatisfier.column):
                    unsatisfier.move(tryrow, trycolumn)
                    if unsatisfier.numConflicts(queens) == bestNumConflicts:
                        candidateNewLocs.append((unsatisfier.row, unsatisfier.column))
                    elif unsatisfier.numConflicts(queens) < bestNumConflicts:
                        candidateNewLocs = []
                        candidateNewLocs.append((unsatisfier.row, unsatisfier.column))
                        bestNumConflicts = unsatisfier.numConflicts(queens)

        # randomly pick a new location from the generated candidates, and move to it
        try:
            loc = choice(candidateNewLocs)
            unsatisfier.move(loc[0], loc[1])
        except:
            # no new locs were generated, so leave the poor queen alone
            pass

    print ("No solution found. Stubborn conflicts: " + str(totalConflicts))
    return False

          

def main():
    # default variables
    numQueens = 8
    maxSteps = 100

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
