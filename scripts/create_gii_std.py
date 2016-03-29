import os, sys, copy
import numpy as np
import nibabel as nib
import epitome as epi
import nibabel.gifti.giftiio
import epitome.commands as cmd

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

## transpose the data so that it is vertices by TR
data = np.transpose(data)
    
    ## if the output is one dimensional, make it 2D
    if len(data.shape) == 1:
        data = data.reshape(data.shape[0],1)
    
    return data

data = load_gii_data(func)
seed = load_gii_data(seed)

# init output vector
rois = np.unique(seed)[1:]
out_data = np.zeros((len(rois), data.shape[1]))

# get mean seed dataistic from each, append to output
for i, roi in enumerate(rois):
    idx = np.where(seed == roi)[0]
        out_data[i,:] = np.mean(data[idx, :], axis=0)

np.savetxt(outputcsv, out_data, delimiter=",")
