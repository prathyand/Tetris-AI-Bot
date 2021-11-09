# Tetris-AI-Bot


It's an AI bot that plays the game of Tetris! It starts of with a blank board. One by one, random pieces
(each consisting of 5 blocks arranged in different shapes) fall from the top of the board to the bottom. As
each piece falls, the player can change the shape by rotating it or fipping it horizontally, and can change its
position by moving it left or right. It stops whenever it hits the ground or another fallen piece. If the piece
completes an entire row, the row disappears and the player receives a point. The goal is for the player to
score as many points before the board fills up.

## Approach:
The first approach was to find the all possible successors of the given piece and use some heuristic function to evaluate the best successor and return the move curresponding to that successor. This approach was initially implemented and tested, however it could be optimized given that we already have the information of the next piece.
### Choice of heuristic function:
Different heuristic functions were tested for the board. The most basic heuristic first tested was the maximum height among heights of all columns. However this did not work very well as two board configurations with same max height were not equally favorable. 
Second approach was to count the void positions on the board those were surrounded by at least one 'x'. More such positions meant less favorable the board configuration. This improved the result over the previous heuristic choice significantly. This approach was then modified using the fact that higher the voids on the board, less favorable is the configuration. And more 'x' around that void, worse is the configuration. The voids trapped under 'x' are essentially worse as the cant be freed until the upper rows are cleared. Hence heuristic gave those voids more weight by raising the power of row number by 4 compared to voids which were blocked only from the sides which used (row number +2) raised to power 2 as a penalty.
Final heuristic was sum of penalties on the board where:
-    If a position on row r blocked form right side:
    penalty = penalty+(r+2) ^2
-    If a position on row r blocked form left side:
    penalty =penalty + (r+2) ^2
-    for a position on row r blocked form top side:
    penalty = penalty + (r+2) ^4

Here +2 is added to row number to avoid 1st row penalty to be same for different cases. (that is 1 ^2 same as 1^ 4)
Following reference was used for this heuristic:
http://kth.diva-portal.org/smash/get/diva2:815662/FULLTEXT01.pdf

### Final algorithm:
The final algorithm used is follows:
First all possible successors of the given board were created. 
All these successors were then passed to a function which, which:
-   created all possible supersuccessors of the given successor of initial board, using the knowledge of next piece.
-   calculated heuristic of all those supersuccessors and returned the min value

Now among all successors of initial board, the move curresponding to the board with lowest supersuccessor was chosen a best move and returned.

### results:
Following best results were obtained during multiple tests:

![p1](https://media.github.iu.edu/user/18306/files/76a2ef80-4025-11ec-8d3a-e22ffaf056f4)


