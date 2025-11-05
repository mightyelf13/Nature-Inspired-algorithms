# Knapsack Genetic Algorithm


## How to Run

**Requirements**  
- The script uses only standard Python libraries (`random` and `sys`). No external installation are needed. However, to get the graph of the fittness it's recommeded to check if matplotlib.pyplot
is installled, in the script the relevant part related to the plotting are commented out, cause they're unreleated to the main task.

**Run the Script**  
- Open either the terminal or command prompt if using windows.
- To run the script with a specific data file, Run:  
   - python knapsack.py input_data.txt
   - Or, python knapsack.py input_data.txt population_size generations; specifying what the size of population one wants and generations the number of gernerations
  
- Replace `input_data.txt` with the path to the input file, if not already in the same path.
- If no file is given, the script will use the default test dataset (debug_10.txt).
- if non populations_size or generations are given, then script will use 100 and 200 respectively, one can if wanted only give population_size, however for this version of the script I haven't
added the intellegence to chose between either, meaning giving only one of whichever one wants.

After the script finishes, it will print:
- **Best total value**: the highest value achieved without exceeding the capacity.
- **Selected items**: the list of items chosen (by index).                       # if wanted this part may be commented out as well, the knapsack funtion will still return them but the values
would simply not be printed.

- **Parameters**: should be noted that the population size and the number of generations are set too 100 and 200 respectively, they can be changed from the main function if one wants too as noted
below the best values were gotten by setting these values to 1000 each.          # In future versions these may be added to the parameter in command line.

## Description of the Algorithm

This script uses the **genetic algorithm** to solve the knapsack problem. The idea behind this algorithm is that we will run the `population` which is made up of solutions called individuals, and
this population will be ran over multiple generations, in order to find the best solution.

### Encoding of Individuals
- Each **individual** is represented as a list of bits (0s and 1s).
- If a bit is 1, the corresponding item is included in the knapsack. If a bit is 0, that item is not included.
- **Example**: If there are 5 items, an individual `[1, 0, 1, 1, 0]` means items 0, 2, and 3 are chosen (which is what would be printed in the **selected items** section; the indices).

### Initial Population
- The initial population is generated randomly (a set of random 0/1 lists).
- Some individuals might violate the weight capacity. Those are **repaired** by removing random items (changing some 1s to 0s) until the total weight is within the capacity limit.

### Fitness Function
- The **fitness** of an individual is the sum of the values of all selected items *if* the total weight does not exceed the knapsack capacity.
- If the individual’s weight is above capacity, its fitness is very low (for example, 0) as a penalty for being an invalid solution.

### Elitism 
   -  Copying of the best inddividual to the next generations to ensure We don't lost them if out operators failed to produce better solutions.

### Selection (Tournament)
- I used **tournament selection** to choose parent individuals for the next generation.
- In tournament selection, a few individuals (for example, 3) are picked at random from the population.
- The one with the highest fitness among this group is selected as a parent.
- This process is repeated to select the parents needed to create new offspring.

### Genetic Operators
**Crossover**  
   - We use one-point crossover to combine two parent solutions, the point is random. 
   - The bits after that point are swapped between two parents to create two new children knows as individuals.
   - **Example** (8-bit individuals, let `|` mark the crossover point):  
     Parent1: `1 0 1 1 | 0 1 0 1`
     Parent2: `0 1 0 0 | 1 1 1 0`
     Child1: `1 0 1 1 1 1 1 0`
     Child2: `0 1 0 0 0 1 0 1`
     (Child1 takes the first part from Parent1 and second part from Parent2, and the opposite for Child2).
**Mutation**
   - After the crossover, every gene in the new individuals has a small chance to **mutate**. This means the bit flips from 0 to 1 or from 1 to 0.
   - This was done so that the mutation could've some diversity in the next population.
**Repair**  
   - If after the crossover and mutation, the child exceeds the capacity. If that happens then the child is **repaired** by removing some items.
   - This is happens by shifting some 1s in the bit string are to 0s  and this repeats until the total weight is under the capacity. This ensures the solution is valid.

### 6. Stopping Criteria

The algorithm stops based on the following conditions:
   - It runs on a fixed number of generations (it's set to can be changed if you want from the script 100 generations).
   - Oor if the population’s solutions have converged early, then the algorithm stops.
   - Then after stoppage it'll return the best solution found (the individual with the highest fitness).

## Sample Results

   - I tested the algorithm on the provided input files and the following are the best results found:                                        **Note: results differed on multiple runs**

   - debug_10.txt: The optimal solution was with a total value of 295. This matched the known optimal value for this test, which mean that the algorithm worked correctly for small
   instances.

   - debug_20.txt: The algorithm achieved the best value of 1024, which matched the optimal given. This tells that even with more items, the algorithm would still reach a correct solution. During
   debbuging we saw that the best fitness in the population increased and hit 1024 before generation 200, then stayed at that value no further improvement, since it found the optimum and hence our
   code ended based on our stopping
   criterias.

   **Note: The results of debug_10 and debug_20 were always the same they never changed and they were 295 and 1024 repectively, however the best solution we chosen for input_100 and input_1000 as
   in some results they differed**

   - input_100.txt: The best solution that was found the algorithm had a total value of approximately 9147.I do not know if this is the exact optimal for this example but since it's esd the 
   largest we reached, then we took 4320. The selceted items for this values were:  [6, 10, 13, 23, 25, 30, 32, 37, 38, 48, 53,60], this was selected 9/10 times of running the code with the 
   following settings: population size: 100 and number of generations 200. Now, note this code was ran on 1000 population size and a 1000 number of generations and the values  was still 9147 which
   gets us to assume that 9147 is indeed the best value achievable.

   - input_1000.txt: Which is the biggest example we got, the the algorithm found the best value around 44794. This result was obtained with a 200 generations to see if it could improve further.
   The fitness curve generally shows improvement generally but every now and then it lowers a bit just to increase in the next generation. The best value was of course 449794 but in genral the 
   solution never fell lower than 40000s and it achievied 44000s 4 times out of 10. By the end of the cycles, the fitness was seen to be in constant between 40000-45000 and thought came my 
   conclusion that this would be the most opotimal no matter how many cycles were to run but in one try for 1000 generations should be noted the script ran for few minutes it achievied a best 
   value of 51733, and the selected iterms were Selected items: [6, 10, 13, 23, 32, 36, 37, 38, 48, 53, 60, 121, 134, 146, 215, 216, 236, 249, 273, 281, 347, 362, 373, 379, 382, 419, 421, 446, 
   463, 469, 473, 476, 480, 493, 494, 523, 573, 592, 599, 603, 610, 612, 643, 657, 669, 673, 703, 708, 718, 732, 736, 739, 743, 770, 775, 786, 821, 822, 824, 830, 845, 855, 883, 886, 914, 937, 
   945, 967, 984, 986, 987, 989]. While we can't be certain this is the absolute optimal for 1000 items, it’s a strong feasible solution given the complexity of the search space. The code was ran 
   on a population size of 1000 and it achieved the following results:  Best total value: 52165 Selected items: [6, 10, 12, 13, 23, 25, 32, 37, 38, 48, 60, 121, 134, 137, 146, 147, 159, 215, 216,
   249, 273, 281, 347, 362, 373, 379, 382, 419, 421, 426, 446, 463, 469, 476, 480, 493, 494, 573, 592, 599, 603, 610, 612, 645, 657, 669, 693, 703, 708, 732, 736, 737, 739, 743, 753, 770, 775, 
   786, 822, 824, 830, 836, 845, 849, 855, 903, 914, 937, 945, 967, 986, 989, 992], Similar values were recived for 1000 generation: Best total value: 50791 Selected items: [10, 23, 25, 32, 35, 
   37, 38, 48, 53, 60, 121, 134, 137, 146, 151, 168, 216, 231, 249, 273, 281, 331, 347, 362, 373, 379, 382, 419, 421, 426, 446, 463, 469, 473, 476, 480, 493, 494, 523, 573, 592, 598, 599, 603, 
   610, 612, 645, 657, 703, 708, 718, 732, 739, 743, 751, 753, 770, 786, 822, 824, 830, 845, 849, 855, 887, 914, 945, 967, 986, 987, 989]. Though the problem with these solutions is that it took a 
   long time for the scrip to run.

The general idea that I got from the code is if one wants the optimal solution go with the higher number of generations or population size and you'll get the optimal solution, hopefullt with very 
small error rate, however if one deserie is a quick program that would return a sub-optimal solutions then 100 population size and 200 number of generation should ok.