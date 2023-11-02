#!/usr/bin/env python
# coding: utf-8
import xnemogcm
import xgcm
import numpy as np
import gsw
import xarray as xr
from pathlib import Path
from skimage.morphology import dilation
from skimage.morphology import disk

xr.set_options(keep_attrs=True)

import sys
exp=sys.argv[1]
#exp='REF_intel'
path_out=('./')

path_in=Path('./')
years=2012
yeare=2018
dim_1D=("t")
Sref=35
rho0=1000

  
for year in range(years,yeare):   
    print(year)
    ds = xnemogcm.open_nemo_and_domain_cfg(nemo_files=list(path_in.glob(f'Maud12t_{year}*.nc')), domcfg_files=['../1_domain_cfg_50levels_new.nc'],nemo_kwargs=dict(datadir='./',chunks={'time_counter':1}))
    ds['bathy_meter']=ds.bathy_meter.swap_dims({'x':'x_c','y':'y_c'})
    ds['x_c'].attrs['axis'] = 'X'
    ds['y_c'].attrs['axis'] = 'Y'        
    ds = ds.drop_vars('ncatice', errors='ignore')
     	
    metrics = {
        ('X',): ['e1t', 'e1u', 'e1v', 'e1f'], # X distances
        ('Y',): ['e2t', 'e2u', 'e2v', 'e2f'], # Y distances
        ('Z',): ['e3t', 'e3u', 'e3v']#, 'e3w'], # Z distances
    }
    grid = xgcm.Grid(ds, metrics=metrics, periodic=False)
        
    # define S_ref
    ds['fw']=(Sref-ds.so)/Sref


    # the freshwater budget is supposed to be computed over the inner domain
    # this means we exclude the outer 4 grid cells in the north, east and west
    # freshwater content Fc= volume integral of ((Sref-S)/Sref)  [m3/s]
    Fc=grid.integrate(ds.fw.isel(x_c=slice(4,291),y_c=slice(0,266)),['X','Y','Z']) 


    

    ds_fwb= xr.Dataset(
           data_vars=dict(Fc=(dim_1D,Fc.data)),
           coords=dict(t=(["t"],ds.t.data))
            )
    ds_fwb.to_netcdf(f'./fw_{year}_EXP_{exp}.nc')  
