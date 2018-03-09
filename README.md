# pyLight


## Maximum Serial Communication Speed
As of Commit 8e5ce86c1c4688e15706bd420becdf4d560769dc
the period of the loop is 3~5 msec ( 200 - 333 Hz ). However a stable reliable 
period is greater than or equal to 0.008 msec (125 Hz). Lower than this can 
cause buffer overflow which can cause incorrect colors to be displayed.

## GUI Workflow
1. Make the GUI using qtDesigner and save it as GUI.ui
1. Run the command `pyuic5 GUI.ui > gui.py` to generate the python gui definition file.
1. Add any slot connections to the `PyLightApp.connect_slots` method in `application.py`
