# ComputationalIntelligence2022
Lab3
- Hard-coded strategies
- I have two hard-coded strategies: 
- The first strategy is that I try to make the total number of remaining matches even so if it is odd, I pick one match from the longest row and if it is already even, if possible, I pick two matches from the longest row (if the longest row contains only one match, I will pick only one)
- The second strategy is that I try to make the total number of active rows even so if it is odd, I pick the whole longest row and if it is already even and the longest row contains n matches, if possible, I pick n-1 matches from the longest row (if the longest row contains only one match, I will pick only one)
- Evolvable strategy
- The strategy is similar to the second hard-coded strategy mentioned above but now first we generate a random number. If the number is lower than the probability p, we pick match(es) from the longest row (according to the above rules) and if it is higher than p, we pick match(es) from the shortest row (according to the same rules). I start with p = 0.5 and then I use 30 generations to evolve the probability p.
- min-max agent
- I used min-max with alpha-betha pruning and it won against the optimal strategy (nim-sum) for number of rows = 1, 2, 3 but when the number of rows goes above 3, the execution of the min-max agent did not terminate.
- Reinforcement learning agent
- I used the first hard-coded strategy mentioned above as the opponent of the RL agent and I evaluated its performance after 4000 matches. Its winning rate in the next 1000 matches was at most about 0.4 which is low but I did not manage to improve it (I also tried multiple different values for alpha and random factor but it did not improve the performance).