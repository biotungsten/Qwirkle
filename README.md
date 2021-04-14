# Qwirkle

This repository contains all code used for my high school research paper on the game theory behind the game of Qwirkle.

## Structure

In the folder _monteCarlo_ you can find the python code used to simulate my formulas. A sample run can be found in the form of the log file of a previous run with ~1250 simulations done.

## Future

The current version has no good performance, this is mainly due to the manual generation and counting of the Qwirkle hands. More efficient algorithms can exclude certain hands from generation, reduce them in size and cut short the time needed to check the remaining hands. Therefore I aim for an implementation iin a more efficient language (e.g. C).
