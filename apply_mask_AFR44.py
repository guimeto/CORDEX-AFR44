# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 02:04:45 2009

@author: guillaume
"""
import xarray as xr
import netCDF4 as nc


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
model = 'HIRHAM5-v1_AFR-44_NCC-NorESM1-M_historical'
variable = 'tasmin'
year = 2005
for year in range(1990,2020):
    for month in range(1,13):
        infile = model + '_' + variable + '_ll_' +  str(year) + '_r.nc'
        #infile = 'HIRHAM5-v1_AFR-44_NCC-NorESM1-M_historical_tasmin_ll_2005_r_'+str(year) +'_{:02d}'.format(int(month))+'_OUTAOUAIS_ERA5grid.nc'           
        outfile = model + '_' + variable + '_ll_' +str(year) + '_M.nc'
        
        nc_Modc=xr.open_dataset(infile)
        data  = nc_Modc[variable].where(mask == 1)
        create_file_from_source(infile, outfile)
