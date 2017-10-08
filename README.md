# pyLight


## Maximum Serial Communication Speed
As of Commit 8e5ce86c1c4688e15706bd420becdf4d560769dc
the period of the loop is 3~5 msec ( 200 - 333 Hz ). However a stable reliable 
period is greater than or equal to 0.008 msec (125 Hz). Lower than this can 
cause buffer overflow which can cause incorrect colors to be displayed.
