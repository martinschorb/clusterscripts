#!/bin/bash

eval "$(/g/emcf/software/python/miniconda/bin/conda shell.bash hook)"
conda activate cluster

python /g/emcf/schorb/code/cluster/fiji_gui.py
