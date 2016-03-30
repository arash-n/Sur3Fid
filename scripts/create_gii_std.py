#!/usr/bin/env python
import os, glob
import numpy as np
import nibabel as nib
import nibabel.gifti.giftiio
import argparse
from subprocess import check_output

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sub", type=str, required=True)
parser.add_argument("-d", "--dir", type=str, default="./")

args = parser.parse_args()

subject=args.sub
dir=args.dir

os.chdir(args.dir)

print("\n")
print ("Current Directory:")
print(os.getcwd() + "\n")
print ("Current Subject:")
print (subject)


def load_gii_data(filename, intent='NIFTI_INTENT_NORMAL'):
    """
        Usage:
        data = load_gii_data(filename)
        
        Loads a gifti surface file (".shape.gii" or ".func.gii").
        
        Returns:
        a 2D matrix of vertices x timepoints,
    """
    ## use nibabel to load surface image
    surf_dist_nib = nibabel.gifti.giftiio.read(filename)
    
    ## gets number of arrays (i.e. TRs)
    numDA = surf_dist_nib.numDA
    
    ## read all arrays and concatenate in numpy
    data = surf_dist_nib.getArraysFromIntent(intent)[0].data
    if numDA >= 1:
        for DA in range(1,numDA):
            data = np.vstack((data, surf_dist_nib.getArraysFromIntent(intent)[DA].data))

hemi="L"

print("\n")
print (hemi+" Hemisphere")
print("\n")

os.chdir(dir+"/"+subject+"/rois/"+hemi)

for file in glob.glob("c_source*.func.gii"):
    
    surf_dist_nib = nibabel.gifti.giftiio.read(filename)
    numDA=surf_dist_nib.numDA
    data=load_gii_data(file)
    print(file+": "+ str(numDA))
    vertices=np.sum(data,axis=0)
    ver=" ".join (map(str,vertices))
    print(str(ver))









