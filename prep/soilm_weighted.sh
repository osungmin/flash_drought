#!/bin/bash

# to compute soil moisture at a specific depth

#example: era5 soil moisture data 
#swvl1: 0 - 7cm       
#swvl2: 7 - 28cm      
#swvl3: 28 - 100cm

#target 0: 0 - 10cm : swvl1 70% + swvl2 30%
#target 1: 0 - 30cm : swvl1 23.33% + swvl2 70.0% + swvl3 6.67%
#target 2: 0 - 50cm : swvl1 14% + swvl2 42% + swvl3 44%

#example: somo.ml soil moisture data
#layer1: 0 - 10 cm
#layer2: 10 - 30cm

#target 2: 0 - 30cm : layer1 33.333% + layer2 66.667%

#
data_path='/your_path_to_input_soilm_data/'

#target depth
layer='swvl30'

if [ "$layer" == "swvl10" ]; then
    c1=0.7
    c2=0.3
    var1="swvl1"
    var2="swvl2"

elif [ "$layer" == "swvl30" ]; then
    c1=0.2333
    c2=0.7
    c3=0.0667
    var1="swvl1"
    var2="swvl2"
    var3="swvl3"

elif [ "$layer" == "swvl50" ]; then
    c1=0.14
    c2=0.42
    c3=0.44
    var1="swvl1"
    var2="swvl2"
    var3="swvl3"

elif [ "$layer" == "swvl100" ]; then
    c1=0.07
    c2=0.21
    c3=0.72
    var1="swvl1"
    var2="swvl2"
    var3="swvl3"
fi

if [ "$layer" == "layer30" ]; then
    c1=0.333
    c2=0.667
    var1="layer1"
    var2="layer2"
fi

if [ "$layer" == "layer50" ]; then
    c1=0.2
    c2=0.4
    c3=0.4
    var1="layer1"
    var2="layer2"
    var2="layer3"
fi


echo
echo $layer $var1 scale factor $c1 and $var2 scale factor $c2 and $var3 scale factor $c3
read $aa


for yr in {2000..2019} ;
 do

   ## prepare file names
   ifile1=${data_path}${var1}/${var1}.1440.720.pentad.${yr}.nc
   ifile2=${data_path}${var2}/${var2}.1440.720.pentad.${yr}.nc
   ifile3=${data_path}${var3}/${var3}.1440.720.pentad.${yr}.nc

   ofile1=${data_path}${var1}/${var1}.weighted.pentad.${yr}.nc
   ofile2=${data_path}${var2}/${var2}.weighted.pentad.${yr}.nc
   ofile3=${data_path}${var3}/${var3}.weighted.pentad.${yr}.nc

   finalfile=${data_path}${layer}/${layer}.1440.720.pentad.${yr}.nc

   ## weighting soil moisure by depth
   if [ ! -f ${ofile1} ]; then
     ls $ifile1
     echo weight factor of ${c1} for ${var1}
     cdo mulc,$c1 $ifile1 $ofile1
   else
     echo already prepared ${ofile1}
   fi

   if [ ! -f ${ofile2} ]; then
     ls $ifile2
     echo weight factor of ${c2} for ${var2}
     cdo mulc,$c2 $ifile2 $ofile2
   else
     echo already prepared ${ofile2}
   fi

   if [ ! -f ${ofile3} ]; then
     ls $ifile3
     echo weight factor of ${c3} for ${var3}
     cdo mulc,$c3 $ifile3 $ofile3
   else
     echo already prepared ${ofile3}
   fi

   ## mean of n-depths soil moisture
   cdo enssum ${ofile1} ${ofile2} ${ofile3} ${data_path}${layer}/imsi.1440.720.${yr}.nc
   #cdo enssum ${ofile1} ${ofile2} ${data_path}${layer}/imsi.1440.720.${yr}.nc

   ## resulted file has a variable name of the first file; will change the variable name.
   cdo chname,${var1},${layer} ${data_path}${layer}/imsi.1440.720.${yr}.nc ${finalfile}
   rm ${data_path}${layer}/imsi.1440.720.${yr}.nc

   rm ${ofile1}
   rm ${ofile2}
   rm ${ofile3}


 done
echo done

