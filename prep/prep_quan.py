#!/usr/bin/env python
import os
import sys
import pandas as pd
import numpy as np
from scipy.stats.mstats import meppf, plotting_positions
import timeit
from netCDF4 import Dataset
print ("modules imported")

def nc_stack(var, ref_yrs): 
    
   ###path to pentad soil moisture netcdfs
   ncpath="/your_path_to_soil_moisture_netcdfs/"
   inpath=ncpath+var+"/"+var+".1440.720.pentad."
   ###

   ###
   print(" \n >>> pentad nc stack ", ref_yrs[0], ref_yrs[-1])
   
   nc_files=[]
   for yr in ref_yrs:
       f = Dataset(inpath+str(yr)+'.nc', 'r')
       nc = f.variables[var][:,:,:].filled(np.nan)
       lats = f.variables['latitude'][:]
       lons = f.variables['longitude'][:]
       if yr==yrs[0]: print(nc.shape, lats[:3], lons[:3])
       f.close()

       print(yr, nc.shape)
       nc_files.append(nc)

   print(" - done.", len(nc_files))
   append = np.concatenate(nc_files, axis=0)
   print(" - appended array shape:", append.shape, "5-day pentad", len(append)/73.)
   return(append)
  
  
def main(array, var, yr, yr0):

   print(" *****")
   print(" - computing percentiles of actual soilm", var)
   print(" - at each grid pixels")
   print()

   #set up start end end pentad for a given year
   yr = int(yr)
   st = 73*(yr-int(yr0)) #yr0 is the first yr considered
   end= st+73 #+1 for python

   #load data
   print(" - soil moisture stacked array ", array.shape)
   print(" - year of", yr, "from-to", st, end)
   yr_array=np.copy(array[st:end,:,:])
   print(" - yr_array:", yr_array.shape)

   #out np.array
   nc_out=np.empty(shape=(yr_array.shape[0], yr_array.shape[1], yr_array.shape[2]))
   nc_out[:,:,:]=np.nan
   print(" - out array:", nc_out.shape)

   print()
   print(" ***** start *****")
   start = timeit.default_timer()
  
   check=0
   for p in range(array.shape[1]):
     for q in range(array.shape[2]):
        
         ### percentile based on the entire yrs
         nc_out[:,p,q]=[meppf(array[x::73,p,q], alpha=0.44, beta=0.44)[yr-yr0] for x in range(73)]
         ###

         if check%2500==0: print("...", check)
         check+=1

   stop = timeit.default_timer()
   print(' - time: ', stop - start)
    
   print("done.")
  
   ###save output
   outpath="/your_path_to_output/"
   np.save(open(outpath+"quan.gringorten."+var+"."+str(yr)+".dat", 'wb'), nc_out, allow_pickle=False)

    
#####
print("give the variable name to compute quantiles")
var=input()
yrs=np.arange(2001, 2020+1, 1)
#####

#load pentad soil moisture data over the period
array=nc_stack(var, yrs)

#compute quantile of soil moisture for all time steps, working on each year
for yr in yrs:
  main(array, var, yr, yrs[0])

print("END.")
