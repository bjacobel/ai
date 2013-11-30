import getopt
import sys
from random import randint, choice, random
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
def run(numQueens, maxSteps, interactive, variant):
    #  create queens (really this is the constraint array, because the 
    #    constraint for each `queen` in `queens` is `queen.isValid(queens) == true`)
    queens = []
    for i in range(0, numQueens):
        queens.append(Queen(i, numQueens))

    start = time.time()
      
    ### RESTARTING VARIANT
    # originalQueens = queens

    # for i in range(4):
    #     queens = originalQueens
    #     for i in range(maxSteps / 4):
    # END RESTARTING VARIANT (it was an undesired change)

    ### ORIGINAL VARIANT:
    for i in range(0, maxSteps):
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

        if variant == "original":
            # randomly find a queen in an invalid position
            unsatisfiers = []
            for queen in queens:
                if not queen.isValid(queens):
                    unsatisfiers.append(queen)
            unsatisfier = choice(unsatisfiers)

        elif variant == "greedy":
            unsatisfiers = []
            worstNumConflicts = 0
            for queen in queens:
                nC = queen.numConflicts(queens)
                if nC == worstNumConflicts:
                    unsatisfiers.append(queen)
                if nC > worstNumConflicts:
                    unsatisfiers = []
                    worstNumConflicts = nC
                    unsatisfiers.append(queen)
            unsatisfier = choice(unsatisfiers)

        elif variant == "random":
            # randomly find a queen in an invalid position
            unsatisfiers = []
            for queen in queens:
                if not queen.isValid(queens):
                    unsatisfiers.append(queen)
            unsatisfier = choice(unsatisfiers)

            if random() <= 0.2:
                unsatisfier.move(randint(0, numQueens))
                continue
        # endif


        ### ORIGINAL VARIANT
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
        ### END ORIGINAL VARIANT

        ### GREEDY SHORTCUT VARIANT (the last one)
        ## This uses the same original variant of picking an unsatisfier as on lines 78-83 above
        # initialConflicts = unsatisfier.numConflicts(queens)
        # for i in range(numQueens):
        #     unsatisfier.move(i)
        #     newConflicts = unsatisfier.numConflicts(queens)
        #     if newConflicts < initialConflicts:
        #         break
        ### END GREEDY SHORTCUT

    print ("No solution found. Stubborn conflicts: " + str(totalConflicts))
    finish = (time.time() - start)*1000
    return False, finish, i

          

def main():
    # default variables
    numQueens = 8
    maxSteps = 500
    interactive = True
    variant = "original"

    # get commandline arguments (if running interactively)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:v:")
    except getopt.GetoptError:
        print("Error in command line parameters. Acceptable options are -n and -v.")
        exit()
    else:
        for opt, arg in opts:
            if opt == "-n":
                numQueens = int(arg)
            if opt == "-v":
                variant = arg

    run(numQueens, maxSteps, interactive, variant)

if __name__ == "__main__":
    main()
