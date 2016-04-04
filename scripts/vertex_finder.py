#!/usr/bin/env python

import numpy as np
import os
import nibabel.gifti.giftiio as gio
import argparse


intent='NIFTI_INTENT_NORMAL'

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--sub", type=str, required=True)
parser.add_argument("-d", "--dir", type=str, default="./")

args = parser.parse_args()

subject=args.sub
dir=args.dir
subdir=dir+"/"+subject+"/"

os.chdir(args.dir)
os.mkdir(subdir+"vertices")


print("\n")
print ("Current Directory:")
print(os.getcwd() + "\n")
print ("Current Subject:")
print (subject)

for hemi in ['L', 'R']:

    myelin_file=subdir+'MNINonLinear/Native/'+subject+"."+hemi+".MyelinMap.native.func.gii"
    out_fname=subdir+"vertices/"+hemi+'_vertices'
    myelin_map=gio.read(myelin_file)
    myelin_vector=myelin_map.getArraysFromIntent(intent)[0].data
    zero_myelin=np.where(myelin_vector == 0)[0]
    nonzero_myelin=np.where(myelin_vector > 0)[0]
    np.savetxt(out_fname, nonzero_myelin+1,fmt='%d')

