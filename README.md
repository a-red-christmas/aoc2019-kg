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
