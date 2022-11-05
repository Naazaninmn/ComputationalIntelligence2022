# ComputationalIntelligence2022
Lab2
-I checked my algorithm many many times but I could not find out what the problem is (At the end the fitness values are not right)
-For each genome the fitness value is the number of covered elements divided by the total number of elements of that genome.
-cross_over function takes one of the subsets included in one parent and substitutes it by one of the subsets included in the other parent and the result would be the offspring.
-mutation function randomly chooses one of the subsets and if the parent includes it, it is removed from the genome and if the parent does not include it, it is added to the genome and the result would be the offspring.