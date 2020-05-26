# -*- coding: utf-8 -*-
"""
Created on Fri Jan  2 02:04:45 2009

@author: guillaume
"""
import xarray as xr
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import numpy as np

def create_dir(directory):
    if not os.path.exists(directory):
        print('Creating Directory '+directory)
        os.makedirs(directory)

#create 2d grid mask http://meteo.unican.es/work/xarray_seminar/xArray_seminar.html

#########################################################
latb = [ 10 , -5 ]
lonb = [ 25 , 40 ]
#########################################################

tomask = ['rainfall(mm.day-1)']
variable = 'rainfall(mm.day-1)'
m_f=xr.open_dataset('mask_ARC2_Ouganda.nc')
lat2d=m_f.variables['lat'][:]
lon2d=m_f.variables['lon'][:]

mask = m_f['region'].values
model = 'ARC2'
path = 'D:/Utilisateurs/guillaume/Desktop/PROJET_AFR44/ARC2/netcdf/'
pathout =  'D:/Utilisateurs/guillaume/Desktop/PROJET_AFR44/ARC2/BOX/'
create_dir(pathout +  model + '/' + variable + '/')

for year in range(2020,2021):
    for month in range(1,13):
        infile = path + model + '_' +  str(year) +f'{month:02}.nc'
        outfile = pathout + model + '_pr_ll_' +  str(year) + '_'+f'{month:02}_M.nc4'
        print(infile)
        nc_Modc=xr.open_dataset(infile)
        data  = nc_Modc[variable].where(mask == 1)
        data = data.sel(lon=slice(*lonb), lat=slice(*latb),)
        data.to_netcdf(outfile)


def plot_background(ax):
    crs_lonlat=ccrs.PlateCarree()
    ax.set_extent([25,40,-5,10])
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
cmap0 = mpl.cm.get_cmap('jet')
cmap0.set_under('w') ## on met en blanc les valeurs inferieures au min de clev
cmap0.set_over('black')
levels = np.arange(0,40.1,2.1) 
mm = ax.contourf(data.lon.values,\
                       data.lat.values,\
                       data[0].values ,\
                       transform=ccrs.PlateCarree(),\
                       cmap=cmap0,
                       levels=levels)
cbar = plt.colorbar(mm, orientation='horizontal', shrink=0.5, drawedges='True', ticks=np.arange(0., 40.1, 2.0),extend='both')
cbar.set_label(u'\n ARC2 - Résolution: 10km', size='medium') # Affichage de la légende de la barre de couleur
cbar.ax.tick_params(labelsize=17)  
    
xticks = np.arange(-150.0,-40.0,20)
yticks =np.arange(10,80,10)    
fig.canvas.draw()            
string_title=u'Uganda mask: ARC2 \n\n  '
plt.title(string_title, size='xx-large')
plt.savefig('OUGANDA_ARC2_PR.png', bbox_inches='tight', pad_inches=0.1)
plt.show()           
