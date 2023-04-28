#!/bin/bash

echo "Running with 4 processes..."
mpiexec -n 4 python main.py --n 4 > output.txt
python showResults.py output.txt
rm output.txt

echo ""
echo "Running with 40 processes..."
mpiexec -n 40 python main.py --n 40 > output.txt
python showResults.py output.txt
rm output.txt