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
for file in sorted(glob.glob("source*_myelin.func.gii")):
    print "Current File Being Processed is: " + file

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
    print(std_myelin_out.shape)
    del data

print("Writing Files...")

myl=nibabel.gifti.giftiio.read(subject+"."+hemi+".MyelinMap.native.func.gii")

newimg=nibabel.gifti.GiftiImage()
darray=std_myelin_out
newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,
intent=myl.darrays[0].intent,datatype=myl.darrays[0].datatype,ordering='F'))
nibabel.gifti.giftiio.write(newimg,subject+"."+hemi+".std_myelin.native.func.gii")

newimg=nibabel.gifti.GiftiImage()
darray=n_vertex
newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,
intent=myl.darrays[0].intent,datatype=myl.darrays[0].datatype,ordering='F'))
nibabel.gifti.giftiio.write(newimg,subject+"."+hemi+".n_vertex.native.func.gii")

newimg=nibabel.gifti.GiftiImage()
darray=mean_myelin_out
newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,
intent=myl.darrays[0].intent,datatype=myl.darrays[0].datatype,ordering='F'))
nibabel.gifti.giftiio.write(newimg,subject+"."+hemi+".n_vertex.native.func.gii")
