# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 02:04:45 2009

@author: guillaume
"""
import xarray as xr
import netCDF4 as nc
import os
def create_dir(directory):
    if not os.path.exists(directory):
        print('Creating Directory '+directory)
        os.makedirs(directory)

def create_file_from_source(src_file, trg_file):
    src = nc.Dataset(src_file)
    trg = nc.Dataset(trg_file, mode='w')

    # Create the dimensions of the file
    for name, dim in src.dimensions.items():
        trg.createDimension(name, len(dim) if not dim.isunlimited() else None)

    # Copy the global attributes
   # trg.setncatts({a:src.getncattr(a) for a in src.ncattrs()})

    # Create the variables in the file
    for name, var in src.variables.items():
        trg.createVariable(name, var.dtype, var.dimensions)

        # Copy the variable attributes
        trg.variables[name].setncatts({a:var.getncattr(a) for a in var.ncattrs()})

        # Copy the variables values (as 'f4' eventually)
        if name not in tomask:
            trg.variables[name][:] = src.variables[name][:]
            
        else:    
            trg.variables[name][:] = data

    # Save the file
    trg.close()

#create 2d grid mask http://meteo.unican.es/work/xarray_seminar/xArray_seminar.html
tomask = ['tasmin']

m_f=xr.open_dataset('mask_AFR44_Ouganda.nc')
lat2d=m_f.variables['lat'][:]
lon2d=m_f.variables['lon'][:]

mask = m_f['__xarray_dataarray_variable__'].values
model = 'CCLM-4-8-17_AFR-44_ECMWF-ERAINT'
variable = 'tasmin'
path = 'D:/Utilisateurs/guillaume/Desktop/PROJET_AFR44/RCM/tasmin/ll/nc/'
pathout =  'D:/Utilisateurs/guillaume/Desktop/PROJET_AFR44/RCM/BOX/'
create_dir(pathout +  model + '/' + variable + '/')

for year in range(1989,1990):
    for month in range(1,13):
        infile = path +  str(year) + '/' + f'{month:02}/' + model + '_' + variable + '_ll_' +  str(year) + '_'+f'{month:02}.nc4'
        outfile = pathout +  model + '/' + variable + '/' + model + '_' + variable + '_ll_' +  str(year) + '_'+f'{month:02}_M.nc4'
        
        nc_Modc=xr.open_dataset(infile)
        data  = nc_Modc[variable].where(mask == 1)
        create_file_from_source(infile, outfile)
        
        
        
