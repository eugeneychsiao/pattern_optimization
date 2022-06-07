# Optimizing Python Code Through Pattern Replacement

Packages used:
-AST
-functools
-astor
-argparse
-timit

This project aims to produce a program that can act as a last step optimization for any .py file. Specific patterns optimized in this project are as follows:
  - replace for loop based string concatenations with .join()
  - replace for loop based list creations with a list comprehension approach
  - initialize object field references locally

To run the program: 
```
python optimize.py filename.py
```
where filename.py is the desired file to be optimized. This will produce 4 optimized files:

  - attr_opti_filename.py
  - join_opti_filename.py
  - comp_opti_filename.py
  - all_opti_filename.py

The  tag at the beginning of the filename corresponds to which type of optimization is applied.

To test the runtime difference of your desired optimized file, run:
```
python timeFiles.py filename.py all_opti_filename.py 100
```
The trailing integer corresponds to the number of runs to measure. The output times will be an average of all the runs.
