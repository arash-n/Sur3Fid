#!/bin/bash
pth=/Applications/workbench/bin_macosx64/

sub=$1
limit=$2


l_surf=${sub}/T1w/Native/${sub}.L.midthickness.native.surf.gii
r_surf=${sub}/T1w/Native/${sub}.R.midthickness.native.surf.gii


num_vert=`${pth}wb_command -file-information ${l_surf}|grep "Number of Vertices"|awk '{print $4}'`

mkdir $sub/vertices
for (( c=0; c<$num_vert; c++ ))
do

echo $c

done>vertices

mkdir ${sub}/rois

${pth}wb_command -surface-geodesic-rois ${l_surf} $limit  vertices ${sub}/rois