import getopt
import sys
from random import randint, choice
from queen import Queen
import time

def drawboard(queens):
    numQueens = len(queens)

    if numQueens > 25:  # cowardly refuse to print grids larger than could possibly fit on the screen
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
# returns True if it succeeded in satisfying all constraints, or False if not
# plus the total time run and the number of moves run for
def run(numQueens, maxSteps, interactive):
    #  create queens (really this is the constraint array, because the 
    #    constraint for each `queen` in `queens` is `queen.isValid(queens) == true`)
    queens = []
    for i in range(0, numQueens):
        queens.append(Queen(i, numQueens))

    start = time.time()

    for i in range(0, maxSteps):
        # print ("run " + str(i))
        totalConflicts = 0
        for queen in queens:
            totalConflicts += queen.numConflicts(queens)

        if totalConflicts == 0:
            finish = (time.time() - start)*1000
            # don't print anything while collecting mass data
            if interactive:
                print ("Solved in {} moves and {:.3f} ms.".format(i, finish))
                drawboard(queens)
            return True, finish, i

        # randomly find a queen in an invalid position
        unsatisfiers = []
        for queen in queens:
            if not queen.isValid(queens):
                unsatisfiers.append(queen)
        unsatisfier = choice(unsatisfiers)

        # try new locations for unsatisfier, find a set of candidate locations that has the same or less conflicts
        bestNumConflicts = numQueens
        originalRow = unsatisfier.row
        candidateNewRows = []
        for tryrow in range(0, numQueens):
            # don't allow staying in the same place
            if tryrow != originalRow:
                unsatisfier.move(tryrow)

                # make a list of all the places that have the same number of conflicts as the least found so far
                if unsatisfier.numConflicts(queens) == bestNumConflicts:
                    candidateNewRows.append(unsatisfier.row)

                # if less conflicts are found, wipe out the list of candidates and start again
                elif unsatisfier.numConflicts(queens) < bestNumConflicts:
                    candidateNewRows = []
                    candidateNewRows.append(unsatisfier.row)
                    bestNumConflicts = unsatisfier.numConflicts(queens)

        # randomly pick a new location from the generated candidates, and move to it
        try:
            unsatisfier.move(choice(candidateNewRows))
        except:
            # no new locs were generated, so leave the poor queen alone
            unsatisfier.move(originalRow)

    print ("No solution found. Stubborn conflicts: " + str(totalConflicts))
    finish = (time.time() - start)*1000
    return False, finish, i

          

def main():
    # default variables
    numQueens = 8
    maxSteps = 500
    interactive = True

    # get commandline arguments (if running interactively)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:")
    except getopt.GetoptError:
        print("Error in command line parameters. Continuing using {} queens.".format(numQueens))
    else:
        for opt, arg in opts:
            if opt == "-n":
                numQueens = int(arg)

    run(numQueens, maxSteps, interactive)

if __name__ == "__main__":
    main()
