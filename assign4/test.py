from __future__ import division
import nqueens

queens = 30
limit = 500
trials = 10

results = []
times = []
runs = []

for i in range(0, trials):
    success, time, moves = nqueens.run(queens, limit)
    results.append(success)
    if success:
        times.append(time)
        runs.append(moves)

print("Success rate: {:.1f}%".format(results.count(True)/trials*100.0))
print("Average time: {:.3f}\nAverage moves: {}".format(sum(times) / float(len(times)), sum(runs) / float(len(runs))))
