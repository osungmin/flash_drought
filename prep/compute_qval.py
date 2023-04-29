#!/usr/bin/env python
import pandas as pd
import numpy as np
from scipy.stats.mstats import mquantiles, plotting_positions
import timeit
from netCDF4 import Dataset
print ("modules imported")

def nc_stack(var, yrs):
   ###
   ncpath="/your_path_to_soil_moisture_pentads"
   inpath=ncpath+var+"/"+var+".1440.720.pentad."
   ###

   print(" \n>>> nc_stack ", yrs[0], yrs[-1])
    
   nc_files=[]
   for yr in yrs:

       f = Dataset(inpath+str(yr)+'.nc', 'r')
       nc = f.variables[var][:,:,:].filled(np.nan)
       lats = f.variables['latitude'][:]
       lons = f.variables['longitude'][:]
       if yr==yrs[0]: print(nc.shape, lats[:3], lons[:3])
       f.close()

       nc_files.append(nc)    

   print(" - done.:", len(nc_files))
   append = np.concatenate(nc_files, axis=0)
   print(" - appended array shape:", append.shape, "5-day pentad", len(append)/73.)
   return(append)
  
if __name__ == '__main__':
   
   #soil moisture variable name
   var='swvl30'
    
   #considered period
   years=np.arange(2001, 2020+1, 1)

   #quantile
   q=.2

   print(" *** start *** ")
   print(" - computing percentiles of", var, years[0], "to", years[-1])
   print(" - quantile:", q)

   #load data
   array=nc_stack(var, years)
   print(" - pentad array shape", array.shape)

   #output data
   nc_out=np.empty([73,array.shape[1],array.shape[2]])
   nc_out[:,:,:]=np.nan
   print(" - output shape:", nc_out.shape)
   print("CLICK!")
   wait=input()
    
   #### main ####
   start = timeit.default_timer()
 
   count=0
   for i in range(array.shape[1]):
       for j in range(array.shape[2]):

           if np.min(array[:,i,j])>0: #land grid pixels only
         
              #output of mquantiiles is a list based on [q]
              nc_out[:,i,j]=[mquantiles(array[x::73,i,j], [q], alphap=.44, betap=.44)[0] for x in range(73)]
      
              if count%2500==0: print(" ...", count)
              if count==0: print(" - just to check, len of n-days?", len(array[0::73,i,j]), len(array[72::73,i,j]))
              count+=1

   print(" - Done.:", q, nc_out.shape)
   print(np.nanmean(np.nanmean(nc_out)))
   print(np.nanmin(np.nanmin(nc_out)), np.nanmax(np.nanmax(nc_out)))
   
   #path_to_save_output
   outpath="/your_path_to_output/"
    
   np.save(open(outpath+"quan"+str(int(q*100))+"."+var+"."+str(years[0])+"-"+str(years[-1])+".dat", 'wb'), nc_out, allow_pickle=False)

print("END.")
 

