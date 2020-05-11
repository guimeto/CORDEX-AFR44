# -*- coding: utf-8 -*-
"""
Created on Thu May  7 21:43:06 2020

@author: guillaume
"""

import numpy as np
import datetime as dt
import xarray as xr
import gdal
from calendar import monthrange

yi = 1983
yf = 2020

for year in range(yi,yf,1):
    for month in ['01','02','03','04','05','06','07','08','09','10','11','12']: 
        days = monthrange(year, int(month))[1]
        for day in range(1,days+1,1):
            # lecture de la serie d ERA5
            try:
                file = './tif/africa_arc.'+str(year)+month+f'{day:02}.tif'
                ds = gdal.Open(file)
                a = ds.ReadAsArray()
                nlat,nlon = np.shape(a)
                
                b = ds.GetGeoTransform() #bbox, interval
                lon = np.arange(nlon)*b[1]+b[0]
                lat = np.arange(nlat)*b[5]+b[3]
                
                
                basedate = dt.datetime(year,int(month),day,0,0,0)
                
                data_set = xr.Dataset( coords={'lon': ([ 'lon'], lon),
                                               'lat': (['lat',], lat),
                                               'time': basedate})
                
                data_set["rainfall(mm.day-1)"] = (['lat', 'lon'],  a)
                
                data_set.to_netcdf( 'ARC2_'+str(year)+month+f'{day:02}.nc') 
            except:
                pass
            