#!/usr/bin/env python
import pandas as pd
import numpy as np
import timeit
from netCDF4 import Dataset
print ("modules imported")

def _load_quans(var, ref_yrs='', q_val=None):
   dirpath="/your_path_to_soilm_quantile_data/" #prepared by compute_qval.py
   with open(dirpath+"quan"+str(int(q_val*100))+"."+var+"."+ref_yrs+".dat", 'rb') as f:
      nc = np.load(f)[:,:,:]
   print(" - load quan:", ref_yrs, q_val, nc.shape)
   return(nc)
  
def nc_stack(var, yrs):
   ###
   ncpath="/your_path_to_soilm_quantile_time_series/"  #prepared by prep_quan.py
   inpath=ncpath+var+"/"+var+".1440.720.pentad."
   ###

   nc_files=[]
   for yr in yrs:

       f = Dataset(inpath+str(yr)+'.nc', 'r')
       nc = f.variables[var][:,:,:].filled(np.nan)
       lats = f.variables['latitude'][:]
       lons = f.variables['longitude'][:]
       if yr==yrs[0]: print(nc.shape, lats[:3], lons[:3])
       f.close()

       nc_files.append(nc)

   print(" - stack pentad array - done.:", len(nc_files))
   append = np.concatenate(nc_files, axis=0)
   print(" - appended array shape:", append.shape,  "5-day pentad", len(append)/73.)
   return(append,lats,lons)
  
  
def detect_fd(var=None, yrs=None, ref_yrs='', quan_norm=None, quan_low=None, quan_end=None, dtime=None):

   #dirpath to input data
   dirpath='/your_path_to_input_data/'

   #open soil quantile
   print(" >>> reading soil moisture pentad over", ref_yrs)
   soilm, lats, lons = nc_stack(var, yrs)
   print(soilm.shape, "for yrs of", yrs[0], yrs[-1], "total:", len(soilm)/73.)

   #open land mask
   print(" > reading land mask info")
   nc=Dataset(dirpath+'static/LandSeaMask.nan.nc', 'r')
   land=nc.variables['lsm'][0,:,:]
   nc.close()
   print(land.shape)

   ###arid_obs
   print(" > loading arid")
   nc = Dataset(dirpath+'static/aridity.2001-2020.nc', 'r')
   arid = nc.variables['snr'][0,:,:].filled(np.nan)
   nc.close()
   print(arid.shape)

   ###temp
   print(" > loading t2m")
   nc = Dataset(dirpath+'static/t2m.monthly.an.era5.1440.720.2001-2020.nc', 'r')
   temp = nc.variables['t2m'][0,:,:].filled(np.nan)
   nc.close()
   print(temp.shape)
  
   ### define keys
   #onset: last pentad above 40 percentile
   #drought_st: first pentad below 20 percentile
   #drought_end: >20p for 2 pentads

   print(" > shape of quantiles")
   print(quan_norm.shape, quan_low.shape, quan_end.shape)

   print()
   keys = ["p", "q", "count", "dr_onset", "dr_st", "dr_end", "ref"]
   dic = {key: list() for key in keys}
   print(" > final keys:", keys)
   print()
   
   ### select land idxs
   i_lands=0
   print(" >>> land selection first")
   p_index, q_index = list(), list()

   for p in range(len(lats)):
      for q in range(len(lons)):

         if arid[p,q]>4: continue #too arid
         if temp[p,q]<273.15: continue #too cold
         if np.nanmean(soilm[:,p,q])<0.01: continue #no land or too dry

         if land[p,q]>0: #mask file contains only land >=0.5 
           p_index.append(p)
           q_index.append(q)
           i_lands+=1

   print(" > land selection - done")
   print("   selected land indices:", i_lands, len(p_index), len(q_index))
   print()
   print("CLICK!")
   #wait=input()


   ### main loop ###
