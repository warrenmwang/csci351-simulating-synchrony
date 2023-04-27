#!/bin/bash

mpiexec -n 4 python main.py --n 4 > output.txt
python showResults.py output.txt
rm output.txt