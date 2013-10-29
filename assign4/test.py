from __future__ import division
import nqueens

queens = 4
limit = 50
trials = 100
results = []

for i in range(0, trials):
    results.append(nqueens.run(queens, limit))

print("Success: {:.1f}%".format(results.count(True)/trials*100.0))