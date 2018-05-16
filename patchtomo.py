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
parser.add_argument('-m', dest='mont', help='use this flag if it is a montaged tomogram', action='store_true', default=False)
parser.add_argument('-d', dest='dual', help='use this flag if it is a dual-axis tomogram', action='store_true', default=False)
parser.add_argument('-b', dest='binning', help='set the binning to be used for image analysis, default is 4', type=int, default=4)



args = parser.parse_args()


# dependencies

import os
import emtools as em
from skimage.transform import downscale_local_mean

# start actions

tf = args.tomofile
binning = args.binning
dir_file = args.directive

if args.mont:
    f = open(dir_file,'a')  
    f.write('setupset.copyarg.montage = 1')
    f.close()

#%%

namebase = tf[:tf.rfind('.')]


# run set up and coarse alignment

if not os.path.exists(namebase+'.preali'):
    callcmd = 'batchruntomo -root \"'+namebase+'\" -directive \"'+args.directive+'\" -current . -end 3 -cp '+str(args.cpus)
    os.system(callcmd)
    
    
# load coarse-aligned stack for finding featureless areas    
instack = em.mrc.mmap(namebase+'.preali')

stacksz = instack.header['nz']

cslice = int(stacksz/2)+1

im = instack.data[cslice,:,:]

# start image analysis

im1 = downscale_local_mean(im,(binning,binning))

from skimage import img_as_float, exposure
from skimage.filters import rank, threshold_otsu
from skimage.morphology import disk, binary_dilation
from skimage.util import invert

from scipy.ndimage import distance_transform_cdt


im1 = em.numpy.rot90(em.numpy.transpose(img_as_float(im1)))
im1 = exposure.rescale_intensity(im1)

selem = disk(7)

im2 = rank.mean(im1,selem = selem)

im3 = im2 > threshold_otsu(im2)

im4 = binary_dilation(im3,selem=selem)

im5 = invert(im4)*1

im5[:,0]=0
im5[:,-1]=0
im5[-1,:]=0
im5[0,:]=0

im6 = distance_transform_cdt(im5)

im7 = im6==1  

em.outline2mod(im7*1, namebase+'_ptbound', z=cslice-1, binning=binning)

f = open(dir_file,'a')  
f.write('runtime.PatchTracking.any.rawBoundaryModel = '+namebase+'_ptbound.mod')
f.close()
    
callcmd = 'batchruntomo -root \"'+namebase+'\" -directive \"'+args.directive+'\" -current . -start 4 -cp '+str(args.cpus)
os.system(callcmd)
    
