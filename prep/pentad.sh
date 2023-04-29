#!/bin/bash
#set -e
#export cdo=/usr/local/bin/cdo-1.4.6

#####
# to prepare pentad soil moisture and/or sutset regions
#####

echo give a variable name
read var
echo $var

### input and output paths
fpath=/your_path_to_input/$var/
outpath=/your_path_to_output/$var/
### period
timesteps=($(seq 1981 1 2020))


if [[ "$var" == "swvl1" ]] ; then
   fname='swvl1.daily.an.era5.1440.720.'
elif [[ "$var" == "layer1" ]] ; then
   fname='layer1.somo_ml_v1.1440.720.'
fi

echo
echo ${var}
echo ${fpath}
echo ${fname}
echo
echo ${outpath}
read $wait

cnt=${#timesteps[@]}

for ((i=0;i<cnt;i++)); do
   echo
   echo ${timesteps[$i]}
   echo

   #remove lunar year
   if (( ${timesteps[$i]} % 4 == 0 )) ; then
     echo lunar year ${timesteps[$i]}
     cdo delete,month=2,day=29 ${fpath}${fname}${timesteps[$i]}.nc ${outpath}${fname}${timesteps[$i]}.nc
   else
     ln -s ${fpath}${fname}${timesteps[$i]}.nc ${outpath}${fname}${timesteps[$i]}.nc  
   fi  
   
   #average to pentad
   cdo timselmean,5 ${outpath}${fname}${timesteps[$i]}.nc  ${outpath}${var}.1440.720.pentad.${timesteps[$i]}.nc 

   rm ${outpath}${fname}${timesteps[$i]}.nc

done

echo
echo PENTAD done for ${var}, check out ${outpath}
echo end.
