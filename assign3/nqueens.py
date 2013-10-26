import getopt
import sys

def drawboard(numQueens):
    if numQueens > 50:
        print("Sorry, drawing the board for a problem of this size isn't practical.")
        return
    qLabel = "Q" + str(numQueens)
    if numQueens < 10:
        qLabel += " "
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



def main():

    numQueens = 8
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:")
    except getopt.GetoptError:
        print("Error in command line parameters. Using 8 queens.")
    else:
        for opt, arg in opts:
            if opt == "-n":
                numQueens = arg
    drawboard(numQueens)


if __name__ == "__main__":
    main()



        