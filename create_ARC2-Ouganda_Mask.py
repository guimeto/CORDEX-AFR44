# -*- coding: utf-8 -*-
"""
Created on Mon May 25 08:57:04 2020

@author: guillaume
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jan  1 20:34:11 2009

@author: guillaume
"""
import xarray as xr
import numpy as np
import regionmask
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl

PATH_TO_SHAPEFILE = './shapefiles/Africa_Countries.shp'
countries = gpd.read_file(PATH_TO_SHAPEFILE)
countries.head()
my_list = list(countries['CODE'])
my_list_unique = set(list(countries['CODE']))
indexes = [my_list.index(x) for x in my_list_unique]
model='D:/Utilisateurs/guillaume/Desktop/PROJET_AFR44/ARC2/netcdf/ARC2_198901.nc'
data = model 
ds = xr.open_mfdataset(data, chunks = {'time': 10})

countries_mask_poly = regionmask.Regions_cls(name = 'COUNTRY', 
                                             numbers = indexes, 
                                             names = countries.COUNTRY[indexes], 
                                             abbrevs = countries.COUNTRY[indexes], 
                                             outlines = list(countries.geometry.values[i] for i in range(0,countries.shape[0])))

mask = countries_mask_poly.mask(ds.isel(time = 0), lat_name='lat', lon_name='lon')
mask.to_netcdf('./mask_ARC2_by_countries.nc')

mask_ouganda = mask.where(mask==758)/mask.where(mask==758)
mask_ouganda.to_netcdf('./mask_ARC2_Ouganda.nc')

np_points  = (mask_ouganda.values  == 1).sum()

plt.figure(figsize=(16,8))
ax = plt.axes()
mask.plot(ax = ax)
countries.plot(ax = ax, alpha = 0.8, facecolor = 'none', lw = 1)
mask.values
    
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

fig = plt.figure(figsize=(28,16))
crs=ccrs.PlateCarree()
ax = plt.axes(projection=crs)
plot_background(ax)

## Choisissons une colormap
cmap0 = mpl.cm.get_cmap('jet_r', 10)
#cmap0.set_under('w') ## on met en blanc les valeurs inferieures au min de clev
#cmap0.set_over('black')
levels = np.arange(0,1.1,0.1) 
mm = ax.contourf(mask_ouganda.lon.values,\
                       mask_ouganda.lat.values,\
                       mask_ouganda.values ,\
                       transform=ccrs.PlateCarree(),\
                       cmap=cmap0,
                       levels=levels)

xticks = np.arange(-150.0,-40.0,20)
yticks =np.arange(10,80,10)    
fig.canvas.draw()    

#cbar = plt.colorbar(mm, orientation='horizontal', shrink=0.75, drawedges='True', ticks=np.arange(0., 1.1, 0.1),extend='both')
#cbar.set_label(u'\n CORDEX-AFR44 mask Ouganda', size='medium') # Affichage de la légende de la barre de couleur
#cbar.ax.tick_params(labelsize=17)  
string_title=u'Uganda mask: gridpoints = ' + str(np_points) + '\n\n  '
plt.title(string_title, size='xx-large')
plt.savefig('OUGANDA_ARC2_Mask.png', bbox_inches='tight', pad_inches=0.1)
plt.show()   