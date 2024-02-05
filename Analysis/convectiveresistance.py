#!/usr/bin/env python
# coding: utf-8
import xnemogcm
import xgcm
import numpy as np
import gsw
import xarray as xr
from pathlib import Path

xr.set_options(keep_attrs=True)

dim_2D = ("y","x")
dim_3D = ("t","y","x")
# import experiment name from bash script
import sys
exp=sys.argv[1]
path_in=Path('./')

# mean density
rho0=1026
g=9.81
for year in range(2016,2018):
    ds = xnemogcm.open_nemo_and_domain_cfg(nemo_files=list(path_in.glob(f'./Maud12t_{year}_grid_T.nc')), domcfg_files=['../1_domain_cfg_50levels_new.nc'],nemo_kwargs=dict(datadir='./'))
    ds['bathy_meter']=ds.bathy_meter.swap_dims({'x':'x_c','y':'y_c'})
    ds['x_c'].attrs['axis'] = 'X'
    ds['y_c'].attrs['axis'] = 'Y'
    ds = ds.drop_vars('ncatice', errors='ignore')
    metrics = {
        ('X',): ['e1t', 'e1u', 'e1v', 'e1f'], # X distances
        ('Y',): ['e2t', 'e2u', 'e2v', 'e2f'], # Y distances
        ('Z',): ['e3t']#, 'e3u', 'e3v', 'e3w'], # Z distances
        }
    grid = xgcm.Grid(ds, metrics=metrics, periodic=False)


    print('computation of the convection resistance (CR) in the upper 830 m, following e.g. Campbell et al. (2019)')
    # CR(H) =g/rho0* int [sigma0(H)-sigma0(z)] dz
    # calculate the potential density 
    ds['sigma']=gsw.sigma0(ds.so,ds.thetao)
       
    # 830 m is depth level (z_c=33)
    Dsigma0=ds.sigma.isel(z_c=33)-ds.sigma
    Dsig_int0_830=grid.integrate(Dsigma0.isel(z_c=slice(0,33)),'Z')
    CR=(g/rho0)*Dsig_int0_830
    CR=CR.rename("CR")
    CR=CR.assign_attrs(long_name='convective resistance of the upper 830m ')
    CR.to_netcdf(f'./cr800_{year}_EXP_{exp}.nc')
