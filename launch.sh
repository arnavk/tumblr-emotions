#!/bin/sh
echo "before source"
source activate /home/nikolaiv/anaconda3/envs/python3/
echo "after source"
python "$1".py
