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

os.chdir(dir)

print("\n")
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

    return data




hemi="L"

print("\n")
print (hemi+" Hemisphere")
print("\n")
print ("Current Directory:")
os.chdir(dir+"/"+subject+"/rois/"+hemi)
print(os.getcwd() + "\n")

n_vertex=np.empty(0)
std_myelin_out=np.empty(0)
mean_myelin_out=np.empty(0)

i=0
for file in glob.glob("source*_myelin.func.gii"):
    data=load_gii_data(file)
    data[data==0]=np.nan
    
    vertices=np.nansum(data,axis=1)
    n_vertex=np.append(n_vertex,vertices)
    
    std_myelin=np.nanstd(data,axis=1)
    std_myelin_out=np.append(std_myelin_out,std_myelin)
    
    mean_myelin=np.nanmean(data,axis=1)
    mean_myelin_out=np.append(mean_myelin_out,mean_myelin)
    
    i=i+1
    print(i)
    del data

print("Writing Files...")

image=nibabel.gifti.giftiio.read(subject+"."+hemi+".MyelinMap.native.func.gii")
intent='NIFTI_INTENT_NORMAL'

image.getArraysFromIntent(intent)[0].data=n_vertex
nibabel.gifti.giftiio.write(image,subject+"."+hemi+".n_vertex.native.func.gii")

image.getArraysFromIntent(intent)[0].data=std_myelin_out
nibabel.gifti.giftiio.write(image,subject+"."+hemi+".std_myelin.native.func.gii")

image.getArraysFromIntent(intent)[0].data=mean_myelin_out
nibabel.gifti.giftiio.write(image,subject+"."+hemi+".mean_myelin.native.func.gii")
