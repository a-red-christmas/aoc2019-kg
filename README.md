# aoc2019-kg
Kaushik Kringle's [AOC 2019](https://adventofcode.com/2019) attempt

# Problems involving the IntCode computer

- [2.1](002.1.cpp) - Basic computer 
- [2.2](002.2.cpp) - First use of a map to dispatch opcodes
- [5.1](005.1.py) - First version in python. Handles immediate and
  reference modes. Indicates error state
- [5.2](005.2.py) - Adds jump instructions - opcodes no longer hard code
  the program counter advance
- [7.1](007.1.py) - Doesn't change the computer, but shows how to run
  several of them separately
- [7.2](007.2.py) - Doesn't change the computer, but shows how to run
  several of them simultaneously, connected to each other
- [9.1](009.1.py) - Adds major modifications to how memory is read and
  written to enable accessing of a core of unspecified size and allows
  offset references. The modification allows for more principled
  resolution of immediate, indirect and indirect offset parameter modes

# Mini-coding diary

## Day 9
As you can see, I switched over to Python by Day 3. I know how to solve
the problems using C++ and I suspect the total amount of code would not
be much more (say 30% more) in terms of lines, but I'm a whole lot
faster in Python.

This is best illustrated by looking at the evolution of the IntCode
computer code which shows how easily the code can be upgraded as the new
requirements come in. In C++ some of the work would be the same, but the
initial abstractions are more costly. 

In the end, after the contest is done, I will write the final version of
the intcode computer in C++ as an exercise.

## Day 12

I could not figure out a solution to Part 2. I'm not sure if some deep
math is needed, or just logic. The solution I came up with a tortoise
and hare type algorithm where we run two simulations in parallel with
one running 2x the other and check to see whenthe 2x simulation jumps
over, or lands on the 1x simulation, but this is too slow - I let it run
overnight and it did not finish. I suspect there is a structure to the
problem that can be exploited. I do note that the axes are independent
of each other, so that is one simplification, but other than that,
without iteratively doing each step, I can not think of a way to
simplify the simulation.


## Day 13
This was a lot of fun. I used a very simple "learning" algorithm to have
a robot player repeatedly play the game until it won. This, however,
needs manual intervention

1. There was some glitch, I think in the "game" itself, where sometimes
   the ball would slip by the paddle. For this, manual intervention was
   needed.
2. Towards the end it is quite easy for the system to fall into an
   infinite loop, with the paddle bouncing the ball back and forth in a
   cycle without encountering any bricks. Manual intervention is needed

A smarter algorithm could be developed that jiggled the computed
solution randomly until further bricks are hit by a move. I did not have
time to code up this solution. Perhaps later...
   
I did implement a caching system ...