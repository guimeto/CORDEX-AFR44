# -*- coding: utf-8 -*-
"""
Created on Mon May 11 14:31:40 2020

@author: guillaume
"""
import xarray as xr
import os 
import glob

# script pour convertir les données en netcdf 
yi = 1983
yf = 2020   
path = 'D:/Utilisateurs/guillaume/Desktop/PROJET_AFR44/ARC2/netcdf/'
for year in range(yi,yf,1):
    for month in ['01','02','03','04','05','06','07','08','09','10','11','12']: 
        
        multi_files = glob.glob(path +'/ARC2_'+str(year)+month+'*.nc' )
        
        ds = xr.concat([xr.open_dataset(f) for f in multi_files], 'time')  
        
        ds.to_netcdf(path + 'ARC2_'+str(year)+month+'.nc')  
        
        [os.remove(f) for f in multi_files]
        
    
            
