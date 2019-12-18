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
one running 2x the other and check to see when the 2x simulation jumps
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

On day 17 I did debug the learning algorithm and does quite well, except
that it eventually gets stuck in a cycle ...

[![Learning 1](http://img.youtube.com/vi/UmLI9LqPXW4/0.jpg)](http://www.youtube.com/watch?v=UmLI9LqPXW4)

[![Learning 2](http://img.youtube.com/vi/vHOktbNpcfk/0.jpg)](http://www.youtube.com/watch?v=vHOktbNpcfk)

[![Learning cycle](http://img.youtube.com/vi/Y1k-22AV-_8/0.jpg)](http://www.youtube.com/watch?v=Y1k-22AV-_8)


## Day 16 (Solving Day 14)

I was surprised by how easy these problems were after battling with
part2 of Day 12 and Day 13. Day 14 Part 2 may have had a clever
solution, I simply used a bracketing bisection to reuse the code I had
written in Part 2, treating the supply network as a black box function.
It converged in around 14 steps.


## Day 16 (attempting Day 13 pt 2)

Ok. I decided to cheat. I'm going to build a "core watcher" program to see what
happens when the ball breaks a brick and then hack the computer to repeatedly
trigger those routines. I'll replay the successful moves I've extracted from
my learning algorithm and then monitor the score, bricks left and the entire
core. Woe betide me if the code has wierd interdependencies and conditionals.

(Plotting score vs balls left gives a reasonably tight trendine but it
is not linear - there is some variation. So it's not possible to predict
the final score exactly from that data)

Inspection of the core reveals two adjacent locations that carry two
interesting pieces of data - the number of balls left and the score.

386 = score and 387 = balls left

What happens if we start off the game, with a set of real scores near
the end of the game and let it keep going??

The last section of the code contains the starting screen.

There are 1012 numbers that form the screen. The next 1012 numbers look
suspiciously like scores. Adding all the numbers corresponding to the
blocks (2) results in 21233 which is declared too high. However, looking
at the scores, the increments are to be found in this table. Also,
replacing all these numbers by 10 or 13 results in the program scoring
the game accordingly. What is missing?

Add up the first 414 scores (20368) is also too high.

Examining the executed instructions via the new logging feature we see
that the scores are not picked from the spots corresponding to the
broken blocks. They are taken from that area of the table, but some
other function is being used to calculate where the score should be
taken from.

e.g if we plot Xs where the first 11 scores come from, we can see they
do not correspond to where the blocks are.

```
############################################
#                                          #
# ** * ***** ****** * *** *  *** **** *  * #
# * * ****  **** ** **********  * *** **** #
# ***  *  * * *    ****** *     * *****X*  #
# ******   *** ** ***  ** * *** ** ******* #
# * ** ** * **  *******X   ** **  **  **** #
# *******  * * *****  * *******    **** *  #
#X*  * * ***** ** * * **  ****X ** *  ***  #
#  ****  X** *** ***** *******    ** ***** #
# * ****** *** * ** *** ***********   ***  #
# * *** * * *X*   ****  ***********  **    #
# * *  ********   ** ***********   *  ** * #
# *** ** ********* **  ***  *** **** * *** #
# ****** ******* ***** * ***** ****  ***** #
# ** ** * **  ***** ** ** **** ** * ****   #
# * *** ****** * ***  ***** * * * * ***  * #
#                                         X#
#                   o                      #
#     X             X     X                #
#    X                                     #
#                     _                    #
#                                          #
```

This suggests that there may be some kind of iterative function that is
being used to pick values from the score table not sequentially, not
based on the the block that is broken, but based on some recurrence
relation. 

We may have to reverse engineer this recurrence relation from the code.

Very likely, this is the code execution that checks for collision,
destroys the brick and then increments the score and decrements the
brick count. My annotations are just below the logs of the relevant
operations

(The log is generated by running `013.2.core-watcher.py`)

```
[ 580] MUL ([2666] -> 16), 44 = 704 => [594]
[ 584] ADD ([2665] -> 24), ([594] -> 704) = 728 => [594]
# These two lines compute the linear offset from the 2D coordinates
# The display is 23 x 44 (rows x cols). [594] <- 44 * row + col

[ 588] ADD 639, ([594] -> 728) = 1367 => [594]
# [594] <- 44 * row * col + 639

[ 592] ADD 0, ([1367] -> 2) = 2 => [2665]
# extract what's at this screen location  

[ 596] RELBASE -3 -> 2664
[ 598] JMP FALSE 0 -> ([2664] -> 279)


[ 279] JMP FALSE ([2665] -> 2) -> NOJMP
# If the screen is empty jump somewhere, but in this case it has a block

[ 282] EQ ([2665] -> 2), 2 : 1 => [381]
# yes, this is a block (2)

[ 286] JMP FALSE ([381] -> 1) -> NOJMP
# If it wasn't a block, jump somewhere, in this case it is a block

[ 289] ADD ([388] -> 25), ([390] -> -1) = 24 => [2665]
[ 293] ADD ([389] -> 17), ([391] -> -1) = 16 => [2666]
# This looks like a move routine, moving the ball. 

[ 297] ADD 0, 304 = 304 => [2664]
[ 301] JMP FALSE 0 -> 393
[ 393] RELBASE 3 -> 2667
[ 395] MUL 1, ([2665] -> 24) = 24 => [2668]
[ 399] MUL ([2666] -> 16), 1 = 16 => [2669]
[ 403] MUL 1, 0 = 0 => [2670]
[ 407] ADD 0, 414 = 414 => [2667]
[ 411] JMP FALSE 0 -> 549
[ 549] RELBASE 4 -> 2671
[ 551] MUL ([2669] -> 16), 44 = 704 => [566]
[ 555] ADD ([2668] -> 24), ([566] -> 704) = 728 => [566]
[ 559] ADD 639, ([566] -> 728) = 1367 => [566]
[ 563] ADD 0, ([2670] -> 0) = 0 => [1367]
[ 567] OUT ([2668] -> 24)
[ 569] OUT ([2669] -> 16)
[ 571] OUT ([2670] -> 0)
[ 573] RELBASE -4 -> 2667
[ 575] JMP TRUE 1 -> ([2667] -> 414)
[ 414] ADD ([2665] -> 24), 0 = 24 => [2668]
[ 418] MUL ([2666] -> 16), 1 = 16 => [2669]
[ 422] ADD 429, 0 = 429 => [2667]
[ 426] JMP TRUE 1 -> 601
[ 601] RELBASE 3 -> 2670
[ 603] MUL 23, ([2668] -> 24) = 552 => [2671]
[ 607] ADD ([2671] -> 552), ([2669] -> 16) = 568 => [2671]
[ 611] MUL 509, 1 = 509 => [2672]
[ 615] MUL 150, 1 = 150 => [2673]
[ 619] ADD 1012, 0 = 1012 => [2674]
[ 623] MUL 630, 1 = 630 => [2670]
[ 627] JMP FALSE 0 -> 456
[ 456] RELBASE 8 -> 2678
[ 458] MUL ([2671] -> 568), ([2672] -> 509) = 289112 => [2675]
[ 462] ADD ([2675] -> 289112), ([2673] -> 150) = 289262 => [2675]
[ 466] MUL ([2674] -> 1012), 64 = 64768 => [2676]
[ 470] LT ([2675] -> 289262), ([2676] -> 64768) : 0 => [381]
[ 474] JMP TRUE ([381] -> 0) -> NOJMP
[ 477] MUL ([2676] -> 64768), -1 = -64768 => [2677]
[ 481] ADD ([2675] -> 289262), ([2677] -> -64768) = 224494 => [2675]
[ 485] LT ([2675] -> 224494), ([2676] -> 64768) : 0 => [381]
[ 489] JMP FALSE ([381] -> 0) -> 481
[ 481] ADD ([2675] -> 224494), ([2677] -> -64768) = 159726 => [2675]
[ 485] LT ([2675] -> 159726), ([2676] -> 64768) : 0 => [381]
[ 489] JMP FALSE ([381] -> 0) -> 481
[ 481] ADD ([2675] -> 159726), ([2677] -> -64768) = 94958 => [2675]
[ 485] LT ([2675] -> 94958), ([2676] -> 64768) : 0 => [381]
[ 489] JMP FALSE ([381] -> 0) -> 481
[ 481] ADD ([2675] -> 94958), ([2677] -> -64768) = 30190 => [2675]
[ 485] LT ([2675] -> 30190), ([2676] -> 64768) : 1 => [381]
[ 489] JMP FALSE ([381] -> 1) -> NOJMP
[ 492] MUL ([2674] -> 1012), 8 = 8096 => [2676]
[ 496] LT ([2675] -> 30190), ([2676] -> 8096) : 0 => [381]
[ 500] JMP TRUE ([381] -> 0) -> NOJMP
[ 503] MUL ([2676] -> 8096), -1 = -8096 => [2677]
[ 507] ADD ([2675] -> 30190), ([2677] -> -8096) = 22094 => [2675]
[ 511] LT ([2675] -> 22094), ([2676] -> 8096) : 0 => [381]
[ 515] JMP FALSE ([381] -> 0) -> 507
[ 507] ADD ([2675] -> 22094), ([2677] -> -8096) = 13998 => [2675]
[ 511] LT ([2675] -> 13998), ([2676] -> 8096) : 0 => [381]
[ 515] JMP FALSE ([381] -> 0) -> 507
[ 507] ADD ([2675] -> 13998), ([2677] -> -8096) = 5902 => [2675]
[ 511] LT ([2675] -> 5902), ([2676] -> 8096) : 1 => [381]
[ 515] JMP FALSE ([381] -> 1) -> NOJMP
[ 518] LT ([2675] -> 5902), ([2674] -> 1012) : 0 => [381]
[ 522] JMP TRUE ([381] -> 0) -> NOJMP
[ 525] MUL ([2674] -> 1012), -1 = -1012 => [2677]
[ 529] ADD ([2675] -> 5902), ([2677] -> -1012) = 4890 => [2675]
[ 533] LT ([2675] -> 4890), ([2674] -> 1012) : 0 => [381]
[ 537] JMP FALSE ([381] -> 0) -> 529
[ 529] ADD ([2675] -> 4890), ([2677] -> -1012) = 3878 => [2675]
[ 533] LT ([2675] -> 3878), ([2674] -> 1012) : 0 => [381]
[ 537] JMP FALSE ([381] -> 0) -> 529
[ 529] ADD ([2675] -> 3878), ([2677] -> -1012) = 2866 => [2675]
[ 533] LT ([2675] -> 2866), ([2674] -> 1012) : 0 => [381]
[ 537] JMP FALSE ([381] -> 0) -> 529
[ 529] ADD ([2675] -> 2866), ([2677] -> -1012) = 1854 => [2675]
[ 533] LT ([2675] -> 1854), ([2674] -> 1012) : 0 => [381]
[ 537] JMP FALSE ([381] -> 0) -> 529
[ 529] ADD ([2675] -> 1854), ([2677] -> -1012) = 842 => [2675]
[ 533] LT ([2675] -> 842), ([2674] -> 1012) : 1 => [381]
[ 537] JMP FALSE ([381] -> 1) -> NOJMP
[ 540] MUL 1, ([2675] -> 842) = 842 => [2671]
[ 544] RELBASE -8 -> 2670
[ 546] JMP FALSE 0 -> ([2670] -> 630)
[ 630] ADD ([2671] -> 842), 1651 = 2493 => [2668]
# 1651 is the code offset that gets us into the score table

[ 634] RELBASE -3 -> 2667
[ 636] JMP TRUE 1 -> ([2667] -> 429)
[ 429] ADD ([2668] -> 2493), 0 = 2493 => [435]
[ 433] ADD ([386] -> 47), ([2493] -> 70) = 117 => [386]
# add points won to current score

[ 437] OUT -1
[ 439] OUT 0
[ 441] OUT ([386] -> 117)
# Print the score

[ 443] ADD ([387] -> 412), -1 = 411 => [387]
# Decrement the ball count

[ 447] JMP TRUE ([387] -> 411) -> 451
```

## Day 17 (attempting Day 13 pt 2)

So, I carried on from where I left off - trying to analyze the code that
computes the score. I tried reverse engineering the formula and did not
have the presence. Then I started to modify the computer core, forcing
it to think that every position was a brick, but none of these worked
properly. The code would add up the wrong scores and so on.

Finally, I tried forcing all the 22nd row positions to masquarade as
paddles i.e I created a giant paddle that spans the width of the board
and this did the trick.

[![Complete cheat](http://img.youtube.com/vi/PdavBT6R6Ak/0.jpg)](http://www.youtube.com/watch?v=PdavBT6R6Ak)


## Day 17 (solving Day 15)

These were FUN! The first part was challenging because of the robot and
in the end I ended up creating clones of the robots (cloning their
brains - had to be careful, the IntCode computer has a bunch of state).
I worried that I would consume to much memory, depending on what the map
looked like - for example if it was a wide open field, I'd end up with a
lot of clones, of the order of the depth. It turns out it's a maze like
map and I think I had at most 5 clones at a time.