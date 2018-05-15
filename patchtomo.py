 # -*- coding: utf-8 -*-

# patchtomo.py

# Copyright (c) 2018, Martin Schorb
# Copyright (c) 2018, European Molecular Biology Laboratory
# Produced at the EMBL
# All rights reserved.


# parse command line parameters

import argparse

parser = argparse.ArgumentParser(description='Tomogram reconstruction on a compute cluster.')
parser.add_argument('tomofile', metavar='F', type=str,
                    help='the tomogram file to process')
parser.add_argument('directive', metavar='D', type=str,
                    help='the batch directive file to use')
parser.add_argument('cpus', metavar='C', type=int,
                    help='the number of CPUs to use')
parser.add_argument('-m', dest='mont', help='use this flag if it is a montaged tomogram', action='store_true', default=False,)




args = parser.parse_args()


# dependencies

import os




# start actions

tf = args.tomofile

namebase = tf[:tf.rfind('.')]


callcmd = 'batchruntomo -root \"'+namebase+'\" -directive \"'+args.directive+'\" -current . -cp '+str(args.cpus)
os.system(callcmd)
