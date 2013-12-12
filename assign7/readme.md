###Value iteration MDP assignment
-----------------

All code is contained in ValueIterationMDP.java, a straightforward Java file. Compile it with `javac *.java`, then run it with `java ValueIterationMDP`and the following options, in order:

1. Discount Factor
2. Max State Utility Error
3. Key Loss Probability
4. Positive Terminal Reward
5. Negative Terminal Reward
6. Step Cost
7. Solution Technique ("sv" or "av" are the allowed options)


For example, to use default parameters, enter the following:

`javac *.java && java ValueIterationMDP 0.99 0.000001 0.5 1 -1 -0.04 sv`