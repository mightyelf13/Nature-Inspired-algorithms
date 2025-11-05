## Ant Colony Optimization (ACO)


**Basic ACO Idea**

- We'll have the  **ants** try all jurneys to serve customers.
- They'll procced to drop **pheromones** on good routes, helping ants in future iterations to choose better paths.
- Over iterations, pheromone trails guide ants toward better and shorter route plans.

**How It Handles VRP:**

- Ants build one route at a time, stopping when the truck is full(capacity has been reached or nothing can be fit the surplus).
- Once full, the ant returns to the depot and starts another route.
- Customers are picked **only if** they can still fit in the truck.
- After every iteration, pheromones are **updated** based on route quality (shorter routes get more).

## Problem Description

The way I've looked at the **Vehicle Routing Problem (VRP)** is as a generalization of the Traveling Salesman Problem (TSP).  Where instead of having a single salesman, we have multiple delivery vehicles with fixed capacity, that we set. The
vehicles must deliver shipments to a set of customers and return to the central depot.

Each problem instance includes:
- A **single depot**
- A set of **customer locations** with demand
- A fleet of **identical vehicles** with limited capacity

The objective is to **serve all customer demands**, using **as few routes** (vehicles) as possible, and **minimizing total travel distance**.

## Algorithm Design: Ant Colony Optimization for VRP

The implemented algorithm follows the ACO design adapted to handle capacity constraints of VRP:

**ACO Basics**
- *Ants* represent agents that build solutions iteratively.
- *Pheromones* are deposited on promising routes to guide future ants.
- A solution is a sequence of routes, each returning to the depot once vehicle capacity is exceeded.

**Adaptations for VRP**
- *Feasibility*: Ants only choose customers whose demand fits the remaining vehicle capacity.
- *Route splitting*: When capacity is full, the ant returns to the depot and starts a new route.
- *Pheromone updates*: Use `Δτ = Q / L` where `L` is the length of the route. Evaporation reduces existing pheromone by a factor ρ.

## Explaining the Code

**`parse_vrp_xml(file_path)`**

- Loads customer coordinates, demands, depot index, and truck capacity from XML.

**`solve_vrp_aco(...)`**

The main ACO routine:
- Builds customer routes for each ant, with respect to the  capacity limits.
- Selects next customer using pheromone + distance.The code to solve the **Vehicle Routing Problem (VRP)** if of course based on **Ant Colony Optimization (ACO)** algorithm. The problem setup is based on the classic CVRPLIB format and 
inputs, from the practivles.

## Code Overview

### `parse_vrp_xml(file_path)`
Parses XML files for:
- Node positions (coordinates)
- Depot location
- Customer demand
- Vehicle capacity

`solve_vrp_aco(...)`
Performs ACO to construct valid vehicle routes:
- Constructs feasible paths respecting demand and capacity
- Applies probabilistic selection using pheromone and distance
- Updates pheromones after each iteration

Parameters include:
- `alpha`, `beta`: Influence of pheromone and distance, respectively
- `rho`: Pheromone evaporation rate
- `Q`: Pheromone constant
- `ants`, `max_iter`: Size of the colonies and the number of iterations     --maximum of course

`visualize_routes(...)`
Uses matplotlib to plot:
- Depot (red star)
- Customers (blue dots)
- Routes (distinct colors)

`run_vrp_instance(file_path)`
Combines everything:
- Parses input
- Runs solver
- Prints solution summary
- Plots result




## How to Run
**Requirements**


**Requirements**  

The script runs on the following libraries:
  - sys
  - xml.etree.ElementTree 
  - numpy
  - matplotlib.pyplot

- The script uses only standard Python libraries (`sys`). No external installation are needed. Now, (`xml.etree.ElementTree `and `numpy`) is usually installed but it should be checked.  However, to get the graph of the fittness it's recommeded to check if matplotlib.pyplot
is installled, in the script the relevant part related to the plotting are commented out, cause they're unreleated to the main task.

  - Installation should be done by either `pip` or `sudo apt` on linux Ubuntu.



**Run the Script**  
- Open either the terminal or command prompt if using windows.
- To run the script with a specific data file, Run:  
   - python vcp.py input_data.xml
   - Or, python knapsack.py input_data.xml number_of_iterations ; specifying how many iteration to be ran.        *Note*: This hasn't been coded yet but hoping will be done

- Replace `input_data.xml` with the path to the input file, if not already in the same path.
- If no file is given, the script will use the default test dataset (dat_32.xml).
- if number of iteration isn't given, then script will use 100.

```bash
python vcp.py filename.xml
```  
```bash
or python vcp.py filename.xml number_of_iterations
```
  - Note: On, linux it may be pyton3 instead of python

It will:
- Load a test XML files- which specified
- Print the best found routes
- Plot a figure showing the vehicle routes

The algorithm  of course only take files like `data_32.xml`, `data_72.xml`, and `data_422.xml` as inputs.





## Sample Results

  - I tested the algorithm on the provided input files and the following are the best results found:                                        **Note: results differed on multiple runs**

  -  `data_32.xml`: graph for this is labeled: (A-n32-k5), the optimal solution found had a total distance traveled is 843 units, side note most slotuion found were between the low 900s and mid 900s and going back to the best solution found the routes were the following: 


  Vehicle 1: 1 -> 28 -> 25 -> 15 -> 27 -> 31 -> 17 -> 2 -> 1
  Vehicle 2: 1 -> 21 -> 6 -> 26 -> 11 -> 16 -> 30 -> 23 -> 10 -> 9 -> 19 -> 1
  Vehicle 3: 1 -> 8 -> 14 -> 22 -> 32 -> 20 -> 18 -> 1
  Vehicle 4: 1 -> 3 -> 4 -> 24 -> 5 -> 12 -> 29 -> 7 -> 1
  Vehicle 5: 1 -> 13 -> 1

  -  `data_72.xml`: graph for this is labeled: (F-n72-k4), the optimal solution found had a total distance traveled is 330.0 units, the solution were mostly between 350-400 and the routes were the following: 

  Vehicle 1: 1 -> 26 -> 25 -> 27 -> 24 -> 30 -> 21 -> 31 -> 22 -> 23 -> 29 -> 28 -> 47 -> 43 -> 45 -> 44 -> 54 -> 46 -> 49 -> 48 -> 51 -> 50 -> 52 -> 71 -> 53 -> 69 -> 40 -> 1
  Vehicle 2: 1 -> 12 -> 2 -> 16 -> 3 -> 14 -> 17 -> 13 -> 18 -> 37 -> 1
  Vehicle 3: 1 -> 55 -> 56 -> 42 -> 58 -> 57 -> 61 -> 62 -> 59 -> 60 -> 64 -> 65 -> 66 -> 63 -> 67 -> 68 -> 38 -> 70 -> 39 -> 41 -> 20 -> 15 -> 19 -> 72 -> 10 -> 4 -> 35 -> 1
  Vehicle 4: 1 -> 33 -> 32 -> 34 -> 36 -> 7 -> 11 -> 6 -> 8 -> 9 -> 5 -> 1
  Now I want to note I once got 317 as distance traveled, but I didn't save the  graph of that trial run so couldn't documented, but here are the routes ofit: 
  Vehicle 1: 1 -> 21 -> 30 -> 24 -> 25 -> 26 -> 27 -> 23 -> 22 -> 31 -> 28 -> 29 -> 47 -> 43 -> 45 -> 44 -> 54 -> 46 -> 49 -> 48 -> 71 -> 52 -> 50 -> 51 -> 53 -> 69 -> 40 -> 1
  Vehicle 2: 1 -> 34 -> 36 -> 37 -> 72 -> 7 -> 11 -> 6 -> 4 -> 10 -> 8 -> 9 -> 5 -> 13 -> 14 -> 18 -> 17 -> 3 -> 20 -> 16 -> 15 -> 60 -> 59 -> 62 -> 66 -> 64 -> 65 -> 35 -> 55 -> 56 -> 42 -> 1
  Vehicle 3: 1 -> 32 -> 33 -> 58 -> 57 -> 61 -> 63 -> 67 -> 68 -> 70 -> 38 -> 39 -> 41 -> 19 -> 1
  Vehicle 4: 1 -> 12 -> 2 -> 1



  -  `data_422.xml`: graph for this is labeled: (B-n422-k3), the optimal solution found had a total distance traveled 2410 units and the distance traveled was again between 2400-2500 the following: 
  Vehicle 1: 421 -> 58 -> 66 -> 55 -> 46 -> 6 -> 53 -> 113 -> 178 -> 233 -> 238 -> 293 -> 353 -> 298 -> 358 -> 421
  Vehicle 2: 421 -> 29 -> 89 -> 34 -> 63 -> 3 -> 22 -> 82 -> 31 -> 32 -> 91 -> 142 -> 92 -> 421
  Vehicle 3: 421 -> 30 -> 4 -> 37 -> 97 -> 64 -> 42 -> 43 -> 102 -> 157 -> 217 -> 162 -> 103 -> 421
  Vehicle 4: 421 -> 291 -> 232 -> 131 -> 172 -> 171 -> 112 -> 11 -> 117 -> 111 -> 52 -> 57 -> 421
  Vehicle 5: 421 -> 105 -> 45 -> 50 -> 51 -> 110 -> 165 -> 125 -> 158 -> 108 -> 49 -> 48 -> 47 -> 98 -> 38 -> 421
  Vehicle 6: 421 -> 54 -> 114 -> 61 -> 73 -> 13 -> 1 -> 18 -> 19 -> 78 -> 133 -> 79 -> 20 -> 421
  Vehicle 7: 421 -> 220 -> 161 -> 160 -> 219 -> 270 -> 244 -> 277 -> 222 -> 163 -> 164 -> 70 -> 421
  Vehicle 8: 421 -> 170 -> 225 -> 230 -> 285 -> 290 -> 345 -> 305 -> 287 -> 338 -> 228 -> 169 -> 168 -> 109 -> 104 -> 44 -> 421
  Vehicle 9: 421 -> 33 -> 8 -> 93 -> 88 -> 87 -> 28 -> 27 -> 86 -> 141 -> 122 -> 134 -> 83 -> 421
  Vehicle 10: 421 -> 16 -> 17 -> 76 -> 77 -> 12 -> 120 -> 119 -> 60 -> 59 -> 118 -> 173 -> 166 -> 115 -> 421
  Vehicle 11: 421 -> 262 -> 211 -> 152 -> 151 -> 202 -> 123 -> 149 -> 94 -> 35 -> 36 -> 9 -> 101 -> 421
  Vehicle 12: 421 -> 126 -> 175 -> 226 -> 235 -> 286 -> 246 -> 306 -> 355 -> 406 -> 415 -> 292 -> 421
  Vehicle 13: 421 -> 65 -> 5 -> 107 -> 218 -> 167 -> 278 -> 227 -> 245 -> 231 -> 177 -> 421
  Vehicle 14: 421 -> 186 -> 72 -> 179 -> 180 -> 239 -> 240 -> 299 -> 413 -> 418 -> 359 -> 421
  Vehicle 15: 421 -> 90 -> 39 -> 40 -> 99 -> 150 -> 124 -> 159 -> 210 -> 100 -> 41 -> 95 -> 155 -> 154 -> 421
  Vehicle 16: 421 -> 96 -> 69 -> 156 -> 215 -> 216 -> 129 -> 221 -> 280 -> 281 -> 340 -> 399 -> 421
  Vehicle 17: 421 -> 176 -> 116 -> 71 -> 327 -> 268 -> 188 -> 273 -> 213 -> 272 -> 331 -> 421
  Vehicle 18: 421 -> 21 -> 81 -> 2 -> 26 -> 62 -> 74 -> 14 -> 23 -> 24 -> 25 -> 84 -> 194 -> 421
  Vehicle 19: 421 -> 146 -> 201 -> 182 -> 254 -> 203 -> 144 -> 67 -> 7 -> 80 -> 85 -> 421
  Vehicle 20: 421 -> 337 -> 282 -> 223 -> 130 -> 229 -> 288 -> 347 -> 398 -> 365 -> 405 -> 350 -> 410 -> 421
  Vehicle 21: 421 -> 185 -> 237 -> 296 -> 295 -> 346 -> 236 -> 352 -> 251 -> 357 -> 356 -> 297 -> 421
  Vehicle 22: 421 -> 183 -> 209 -> 269 -> 214 -> 243 -> 329 -> 274 -> 303 -> 322 -> 271 -> 153 -> 421
  Vehicle 23: 421 -> 362 -> 374 -> 323 -> 264 -> 205 -> 127 -> 200 -> 259 -> 318 -> 373 -> 313 -> 258 -> 421
  Vehicle 24: 421 -> 10 -> 276 -> 335 -> 394 -> 389 -> 334 -> 275 -> 189 -> 249 -> 421
  Vehicle 25: 421 -> 140 -> 199 -> 253 -> 198 -> 139 -> 138 -> 193 -> 121 -> 174 -> 135 -> 234 -> 294 -> 195 -> 136 -> 421
  Vehicle 26: 421 -> 267 -> 208 -> 128 -> 68 -> 147 -> 206 -> 261 -> 242 -> 314 -> 421
  Vehicle 27: 421 -> 408 -> 370 -> 409 -> 310 -> 404 -> 403 -> 344 -> 250 -> 349 -> 421
  Vehicle 28: 421 -> 75 -> 15 -> 255 -> 196 -> 132 -> 137 -> 197 -> 256 -> 315 -> 414 -> 361 -> 378 -> 421
  Vehicle 29: 421 -> 289 -> 348 -> 407 -> 411 -> 412 -> 371 -> 416 -> 417 -> 311 -> 351 -> 421
  Vehicle 30: 421 -> 366 -> 191 -> 252 -> 360 -> 317 -> 376 -> 375 -> 316 -> 257 -> 421
  Vehicle 31: 421 -> 106 -> 56 -> 300 -> 419 -> 420 -> 312 -> 377 -> 372 -> 307 -> 421
  Vehicle 32: 421 -> 190 -> 224 -> 283 -> 397 -> 342 -> 304 -> 364 -> 390 -> 339 -> 279 -> 421
  Vehicle 33: 421 -> 336 -> 395 -> 309 -> 401 -> 396 -> 369 -> 400 -> 341 -> 402 -> 343 -> 284 -> 421
  Vehicle 34: 421 -> 184 -> 330 -> 324 -> 265 -> 187 -> 260 -> 319 -> 320 -> 379 -> 380 -> 385 -> 421
  Vehicle 35: 421 -> 143 -> 266 -> 321 -> 302 -> 263 -> 204 -> 145 -> 247 -> 325 -> 384 -> 383 -> 386 -> 421
  Vehicle 36: 421 -> 212 -> 363 -> 382 -> 332 -> 391 -> 392 -> 333 -> 248 -> 328 -> 387 -> 421
  Vehicle 37: 421 -> 181 -> 241 -> 354 -> 301 -> 192 -> 381 -> 326 -> 148 -> 421
  Vehicle 38: 421 -> 367 -> 368 -> 393 -> 308 -> 388 -> 207 -> 421



  **Graphs**:  I've presented two graphs for each example one represents the convergence graphs asked for, the other represents the the routes taken and the informatino have been mentioned already.