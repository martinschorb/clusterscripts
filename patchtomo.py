 # -*- coding: utf-8 -*-

# patchtomo.py

# Copyright (c) 2018, Martin Schorb
# Copyright (c) 2018, European Molecular Biology Laboratory
# Produced at the EMBL
# All rights reserved.


import argparse

parser = argparse.ArgumentParser(description='Tomogram reconstruction on a compute cluster.')
parser.add_argument('tomofile', metavar='F', type=str,
                    help='the tomogram file to process')

parser.add_argument('-m', dest='mont', help='use this flag if it is a montaged tomogram', action='store_true', default=False,)


args = parser.parse_args()

print(args.mont)