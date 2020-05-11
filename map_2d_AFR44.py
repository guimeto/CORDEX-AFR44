
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 08:51:04 2020

@author: guillaume
"""
from netCDF4 import Dataset
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np 
import matplotlib as mpl
import pandas as pd
import gc
gc.collect()

def plot_background(ax):
    crs_lonlat=ccrs.PlateCarree()
    ax.set_extent([-20,60,-35,35])
    ax.coastlines(resolution='110m');     
    ax.add_feature(cfeature.LAKES.with_scale('50m'))     
    ax.add_feature(cfeature.BORDERS.with_scale('50m'))    
    ax.add_feature(cfeature.RIVERS.with_scale('50m'))    
    coast = cfeature.NaturalEarthFeature(category='physical', scale='10m',    
                        facecolor='none', name='coastline')
    ax.add_feature(coast, edgecolor='black')
    ax.gridlines(crs=crs_lonlat,
                 xlocs = np.arange(-180,180,15),
                 ylocs = np.arange(-180,180,15),
                 draw_labels = True)   
    return ax

Y=np.array([[51,51,0],[51,102,0],[102,102,51],[102,153,51],[153,204,102],[153,255,158],[204,255,153],[204,255,204],\
            [153,0,255],[153,51,255],[153,102,255],[102,51,204],[51,0,153],[0,51,153],[51,102,204],[102,153,255],\
            [31,255,255],[102,255,255],[153,255,255],[204,255,255],\
            [255,255,204],[255,255,102],[255,255,0],[255,204,102],[255,204,51],[255,204,0],\
            [255,153,51],[255,102,0],[255,51,0],[255,51,51],[255,0,0],[204,51,51],\
            [204,0,0],[153,51,51],[153,0,0],[102,51,51],[102,0,0],[102,51,0],[51,0,0],[0,0,0]])/255.
    
colbar=mpl.colors.ListedColormap(Y)
colbar=mpl.colors.ListedColormap(Y)
    
yi = 1990
yf = 2019
#########################################################
file = 'HIRHAM5-v1_AFR-44_NCC-NorESM1-M_historical_tasmin_ll_2005_r.nc'


dset=Dataset(file)
## Lecture du fichier 1 er pas de temps 
var=dset.variables['tasmin'][0][:] - 273.15
lon=dset.variables['lon'][:]
lat=dset.variables['lat'][:]

fig = plt.figure(figsize=(28,16))
cmap0 = mpl.cm.get_cmap('jet', 20)
#    cmap0.set_under('darkblue') 
#    cmap0.set_over('darkred')

crs=ccrs.PlateCarree()
ax = plt.axes(projection=crs)
plot_background(ax)
mm = ax.contourf(lon,\
                   lat,\
                   var,\
                   vmin=0,\
                   vmax=40, \
                   transform=ccrs.PlateCarree(),\
                   levels=np.arange(0, 40.1, 2.0),\
                   cmap=cmap0 ,
                   extend='both')

#    mm = ax.pcolormesh(lon,\
#                       lat,\
#                       var,\
#                       vmin=-28,\
#                       vmax=28, \
#                       transform=ccrs.PlateCarree(),\
#                       cmap=cmap0 )
mm.cmap.set_over('darkred')
mm.cmap.set_under('darkblue')   
#    ax.contour(ds_all.variables['lon'][:], ds_all.variables['lat'][:], data_clim, 
 #                             levels = np.arange(-28, 28.1, 4.0), 
  #                            linewidths=1, 
   #                           colors='k',
#                          transform = ccrs.PlateCarree())


cbar = plt.colorbar(mm, orientation='vertical', shrink=0.75, drawedges='True', ticks=np.arange(0, 40.1, 2),extend='both')
cbar.set_label(u'\n Projection =  CORDEX-AFR44 / Created by Guillaume Dueymes', size='medium') # Affichage de la légende de la barre de couleur
cbar.ax.tick_params(labelsize=17) 
string_title=u'HIRHAM5-v1_AFR-44_NCC-NorESM1-M_historical_tasmin 01/01/2005 \n\n  '
plt.title(string_title, size='xx-large')
plt.savefig('HIRHAM5-v1_AFR-44_NCC-NorESM1-M_historical_tasmin_ll_20050101.png', bbox_inches='tight', pad_inches=0.1)

