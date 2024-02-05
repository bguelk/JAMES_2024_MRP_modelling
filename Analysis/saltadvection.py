#!/usr/bin/env python
# coding: utf-8
import xnemogcm
import xgcm
import numpy as np
import gsw
import cmocean.cm as cmo
import xarray as xr
from pathlib import Path
from skimage.morphology import dilation
from skimage.morphology import disk
import matplotlib.pyplot as plt
xr.set_options(keep_attrs=True)

import sys
exp=sys.argv[1]
path_out=('./')

path_in=Path('./')
 
#print(year)
ds = xnemogcm.open_nemo_and_domain_cfg(nemo_files=list(path_in.glob(f'Maud12t_201[6,7]*.nc')), domcfg_files=['../1_domain_cfg_50levels_new.nc'],nemo_kwargs=dict(datadir='./',chunks={'time_counter':1}))
ds['bathy_meter']=ds.bathy_meter.swap_dims({'x':'x_c','y':'y_c'})
ds['x_c'].attrs['axis'] = 'X'
ds['y_c'].attrs['axis'] = 'Y'        
ds = ds.drop_vars('ncatice', errors='ignore')
ds.coords['year']=ds.t.dt.year     	

ds['somean']=ds.so.mean(dim='t')


metrics = {
    ('X',): ['e1t', 'e1u', 'e1v', 'e1f'], # X distances
    ('Y',): ['e2t', 'e2u', 'e2v', 'e2f'], # Y distances
    ('Z',): ['e3t', 'e3u', 'e3v']#, 'e3w'], # Z distances
}
grid = xgcm.Grid(ds, metrics=metrics, periodic=False)
deptht=ds.e3t_1d.cumsum(dim='z_c')#- 0.5*ds.e3t_1d.isel(z_c=0)
deptht=deptht.rename("deptht")

# compute salt content the upper 100m 
sanomaly=ds.so-ds.somean
sa_100=(sanomaly*ds.e3t).where(deptht<100).sum('z_c')/(ds.e3t.where(deptht<100).sum('z_c'))
u_100=(ds.uo*ds.e3u).where(deptht<100).sum('z_c')/(ds.e3u.where(deptht<100).sum('z_c'))
v_100=(ds.vo*ds.e3v).where(deptht<100).sum('z_c')/(ds.e3v.where(deptht<100).sum('z_c'))
ds['u_100']=u_100.fillna(0)
v_100=grid.interp(v_100.fillna(0),['X','Y'],boundary='extend')


ds['sa_100']=sa_100#.fillna(0)
ds['u_100']=u_100.fillna(0)
ds['v_100']=v_100

ds.u_100.to_netcdf(f'./u100_saltadv_{exp}.nc')
ds.v_100.to_netcdf(f'./v100_saltadv_{exp}.nc')
ds.sa_100.to_netcdf(f'./sa100_saltadv_{exp}.nc')


