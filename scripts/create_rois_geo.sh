#!/bin/bash
pth=/Applications/workbench/bin_macosx64/

sub=$1
limit=$2

mkdir $sub/rois
mkdir $sub/vertices
mkdir $sub/vars


hemi=L

surf=${sub}/MNINonLinear/Native/${sub}.${hemi}.midthickness.native.surf.gii

mkdir ${sub}/rois/${hemi}
mkdir ${sub}/vertices/${hemi}
mkdir $sub/vars/${hemi}

num_vert=`${pth}wb_command -file-information ${surf}|grep "Number of Vertices"|awk '{print $4}'`

for (( c=0; c<$num_vert; c++ ))
do

echo $c

done>$sub/vertices/${hemi}/vertices
(
cd $sub/vertices/$hemi
split vertices source
)

${pth}wb_command -metric-math 'y>0' $sub/rois/$hemi/mask.func.gii -var y ${sub}/MNINonLinear/Native/${sub}.L.MyelinMap.native.func.gii

for a in ${sub}/vertices/${hemi}/source??

do

i=`basename $a`

${pth}wb_command -surface-geodesic-rois ${surf} $limit  $sub/vertices/$hemi/$i ${sub}/rois/$hemi/${i}.func.gii

${pth}wb_command -metric-math 'x*y' $sub/rois/$hemi/${i}_myelin.func.gii -var x ${sub}/rois/$hemi/${i}.func.gii -var y ${sub}/MNINonLinear/Native/${sub}.L.MyelinMap.native.func.gii -repeat

${pth}wb_command -metric-math 'x*y' ${sub}/rois/$hemi/c_${i}.func.gii -var x ${sub}/rois/$hemi/${i}.func.gii -var y $sub/rois/$hemi/mask.func.gii -repeat

${pth}wb_command -metric-stats $sub/rois/$hemi/${i}_myelin.func.gii -reduce COUNT_NONZERO -roi ${sub}/rois/$hemi/c_${i}.func.gii -match-maps>>NONzero.txt
${pth}wb_command -metric-stats $sub/rois/$hemi/${i}_myelin.func.gii -reduce MEAN -roi ${sub}/rois/$hemi/c_${i}.func.gii -match-maps>>MEAN.txt
${pth}wb_command -metric-stats $sub/rois/$hemi/${i}_myelin.func.gii -reduce STDEV -roi ${sub}/rois/$hemi/c_${i}.func.gii -match-maps>>STD.txt

done