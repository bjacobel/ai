from __future__ import division
import nqueens

nqueens_to_test = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
limit = 500
trials = 10

for queens in nqueens_to_test:
    results = []
    times = []
    runs = []

    for i in range(0, trials):
        success, time, moves = nqueens.run(queens, limit, False, "original")
        results.append(success)
        if success:
            times.append(time)
            runs.append(moves)

    print("Did {} trials with {} queens.".format(trials, queens))
    print("Success rate: {:.1f}%".format(results.count(True)/trials*100.0))
    print("Average time: {:.3f}\nAverage moves: {}\n".format(sum(times) / float(len(times)), sum(runs) / float(len(runs))))
