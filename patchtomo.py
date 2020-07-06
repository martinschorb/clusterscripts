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
parser.add_argument('-u', dest='user', help='who runs this (for email notification)', type=str)



args = parser.parse_args()
tf = args.tomofile
binning = args.binning
dir_file = args.directive
cpus = args.cpus
dual = args.dual
user = args.user

if args.mont:
    f = open(dir_file,'a')  
    f.write('setupset.copyarg.montage = 1\n')
    f.close()

#%%

# dependencies

import os
import numpy
import pyEM as em
from skimage.transform import downscale_local_mean
from skimage.filters import threshold_otsu


# start actions



def exclude_bright_area(im1):
#    generates an outline image around areas that can be used for patch tracking
#    this can then be used in outline2mod to create a boundary model
#    bright uniform areas (empty resin) are excluded
    
    from skimage import img_as_float, exposure
    from skimage.filters import rank
    from skimage.morphology import disk, binary_dilation
    from skimage.util import invert    
    from scipy.ndimage import distance_transform_cdt
        
    im1 = numpy.rot90(numpy.transpose(img_as_float(im1)))
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
    
    return im7

def hasdark(im,deviation = 2,areafraction = 0.03):
#    determines whether an image has large dark areas
#   deviation is multiples of std to check          
 
    im2=im.astype(float)
    im3=im2-im2.min()
    dark = im3<im3.mean()-deviation*im3.std()
    return numpy.sum(dark)>numpy.prod(numpy.array(im3.shape)) * areafraction
    
    


#%%

namebase = tf[:tf.rfind('.')]
base1=namebase
namebase1=list()
namebase1.append(namebase)

adoc=em.loadtext(dir_file)

if dual :    
    namebase = tf[:tf.rfind('a.')]
    base1=namebase
    namebase1.append(namebase+'b')    
# run set up and coarse alignment

if (not os.path.exists(namebase1[0]+'.preali')):
    callcmd = 'batchruntomo -root \"'+base1+'\" -directive \"'+dir_file+'\" -current . -end 3 -cp '+str(cpus)
    os.system(callcmd)

for nb in namebase1:    

    
    # load coarse-aligned stack for finding featureless areas    
    instack = em.mrc.mmap(nb+'.preali')
    
    stacksz = instack.header['nz']
    
    cslice = int(stacksz/2)+1
    
    im = instack.data[cslice,:,:]
    
    currslice = 0
    exclude=list()
    while hasdark(instack.data[currslice,:,:]):
        currslice = currslice + 1
        exclude.append(currslice)
    
    currslice = -1
    while hasdark(instack.data[currslice,:,:]):
        currslice = currslice - 1
        exclude.append(currslice)
        
    exclude.sort()
    
    skipline=[line for line in adoc if "setupset.copyarg.skip" in line]    
    
    delim=' '
    if len(skipline)>0:
      if not skipline[-1][-1]=='=': delim=','
    
      adoc[adoc.index(skipline[0])]=skipline[-1]+delim+','.join(list(map(str,exclude)))
    
    # start image analysis
    
    im1 = downscale_local_mean(im,(binning,binning))
    
    im7 = exclude_bright_area(im1)
    
    em.outline2mod(im7*1, nb + '_ptbound', z=cslice-1, binning=binning)
    f = open(dir_file,'a')
    f.write('\n')
    if dual:
      if nb==namebase1[0]:
          f.write('runtime.PatchTracking.a.rawBoundaryModel = '+nb+'_ptbound.mod\n')
      else:
          f.write('runtime.PatchTracking.b.rawBoundaryModel = '+nb+'_ptbound.mod\n')
    else:
      f.write('runtime.PatchTracking.any.rawBoundaryModel = '+nb+'_ptbound.mod\n')
    f.close()


    
callcmd = 'batchruntomo -root \"'+base1+'\" -directive \"'+ dir_file +'\" -current . -start 4 -cp '+str(cpus)+' -em ' +user+ '@embl.de'
os.system(callcmd)
    
