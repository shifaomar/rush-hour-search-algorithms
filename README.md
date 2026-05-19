# Rush Hour Solver

A Python implementation of the classic Rush Hour puzzle using Breadth-First Search (BFS) and heuristic-based Best-First Search algorithms. This project explores state-space search, heuristic design, and performance analysis for solving constrained puzzle environments.

## Overview

The goal of the Rush Hour puzzle is to move the red car (X) to the exit by shifting blocking vehicles within a 6×6 grid.

This project implements:

Breadth-First Search (BFS)
Best-First Search with Heuristic 1 (H1)
Best-First Search with Heuristic 2 (H2)

and compares their performance based on:

number of visited nodes
search efficiency
heuristic effectiveness

The project also includes custom puzzle generation and difficulty analysis.

## Features
Solves Rush Hour boards using multiple search algorithms
Implements admissible heuristics
Tracks visited states to avoid repeated exploration
Compares search-space size across algorithms
Generates graphs and performance metrics
Includes custom-designed difficult puzzle boards
## Algorithms
### Breadth-First Search (BFS)

The BFS solver explores states level-by-level using a queue.
Each board configuration is stored as an immutable tuple and tracked in a visited set.

Because all moves have equal cost, BFS guarantees the shortest possible solution path.

### Heuristic 1 (H1)

Estimates the remaining cost using:

the number of columns between the red car and the exit

This heuristic is admissible because it never overestimates the true cost.

### Heuristic 2 (H2)

Extends H1 by also considering:

the number of blocking vehicles in the exit row

This heuristic is more informed and consistently produces estimates equal to or higher than H1 while remaining admissible.

### Performance Comparison

Average nodes visited across 40 puzzles:

#### Algorithm	Average Nodes Visited
BFS	3238
H1	2850.875
H2	2610.675

Example puzzle results:

#### Puzzle	BFS	H1	H2
Beginner (01)	1077	1067	1045
Advanced (23)	2823	2408	2028
Expert (31)	3999	3946	3840

Results showed that heuristic-based search significantly reduced the search space compared to brute-force BFS, with H2 performing best overall by accounting for blocking vehicles.

## Custom Puzzle Design

Custom boards were designed by:

placing the red car
adding blocking vehicles
adding additional dependencies that blocked those vehicles

This created layered dependencies that increased:

solution depth
branching complexity
search-space size

One custom board required over 20,000 visited nodes using BFS.

## Technologies Used
Python
Data Structures (queues, priority queues, sets)
State-Space Search
Heuristic Search
Matplotlib (for visualization)
## Example Topics Demonstrated
Breadth-First Search
Best-First Search
Admissible heuristics
State representation
Search optimization
Puzzle solving AI
Performance analysis
## How to Run
python rushhour.py

The program will:

load puzzle boards
run BFS, H1, and H2
output solution statistics and visited node counts
generate performance comparisons
## Files
rushhour.py         # Main solver implementation
boards.txt          # Puzzle board definitions
