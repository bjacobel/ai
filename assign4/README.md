####README
------
This project contains code that implements the local search algorithm for the N-Queens problem.

The code is Python, and has been tested on version 2.7.3. It should run on Python 3, but I haven't tested it.

To run the code, enter the command

	python nqueens.py -n <number-of-queens> -v <original|greedy|random> -r <smarter|restarts|firstbetter>

If you do not specify the *-n* command line switch for the number of queens, 8 queens will be used.

Likewise, if you do not specify the -v command line switch, the original implementation of the algorithm will be used. You may alternately specify the greedy or random variants in this way.

Likewise, if you do not specify the -r command line switch, none of the variants wherein initial placement is smarter, the algorithm restarts, of the algorithm takes a "first-better" greedy shortcut will be taken.


The file test.py contains code to run the program multiple times and compile the results. To run it:

	python test.py

Variables such as number of iterations, number of queens and so forth are hard-coded in this file.



#####--Brian Jacobel, 10/26/13