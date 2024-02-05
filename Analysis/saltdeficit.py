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
import scipy

xr.set_options(keep_attrs=True)

dim_2D = ("y","x")
dim_3D = ("t","y","x")
# import experiment name from bash script
import sys
exp=sys.argv[1]
path_in=Path('./')
#heat capacity of seawater
cw=4000#grid.average(gsw.cp_t_exact(ds.so,ds.thetao,0),['Z','Y','X']).mean(dim='t')
# mean density
rhow=1026#grid.average(ds.sigma,['X','Y','Z']).mean(dim={'t'})
rhoi=900
Li=2.5e5
# calculate the salinity difference between ocean surface and sea ice
DSi=30#ds.so.isel(z_c=0)-4
alpha=0.43*10**-4
beta=7*10**-4


for year in range(2013,2018):
    print(year)
    ds = xnemogcm.open_nemo_and_domain_cfg(nemo_files=list(path_in.glob(f'./Maud12t_{year}_grid_T.nc')), domcfg_files=['../1_domain_cfg_50levels_new.nc'],nemo_kwargs=dict(datadir='./'))
    ds['bathy_meter']=ds.bathy_meter.swap_dims({'x':'x_c','y':'y_c'})
    # reduce the region for computational reasons
    ds['x_c'].attrs['axis'] = 'X'
    ds['y_c'].attrs['axis'] = 'Y'
    ds = ds.drop_vars('ncatice', errors='ignore')
    metrics = {
        ('X',): ['e1t', 'e1u', 'e1v', 'e1f'], # X distances
        ('Y',): ['e2t', 'e2u', 'e2v', 'e2f'], # Y distances
        ('Z',): ['e3t']#, 'e3u', 'e3v', 'e3w'], # Z distances
        }
    grid = xgcm.Grid(ds, metrics=metrics, periodic=False)
    print('computation of Salt Deficit and Thermal Barrier')

    # compute freezing temperature of seawater at surface
    ds['tf']=gsw.CT_freezing(ds.so.isel(z_c=0),0,0.1)
    deltaS=ds.so.isel(z_c=33)-ds.so.isel(z_c=0)
    deltaT=ds.thetao.isel(z_c=33)-ds.tf
    hi=(ds.mldr10_1/DSi)*(deltaS- (alpha/beta)*deltaT) 
    hi=hi.rename("hi")
    hi=hi.assign_attrs(long_name='Ice growth necessary to deep convect')
    hi.to_netcdf(f'./hi800_{year}_EXP_{exp}.nc')
    



