#!/usr/bin/env python
# coding: utf-8
import numpy as np
import xarray as xr
xr.set_options(keep_attrs=True)
import sys
exp=sys.argv[1]

ds=xr.open_dataset('./ymonmean2.nc')

# create a climatology for the Region of Maud Rise (according to Wilson et al. 2019;  2W-8E, 64S-6S)
ds_wilson=ds.where((ds.nav_lon_grid_T >-2)&(ds.nav_lon_grid_T<8)&(ds.nav_lat_grid_T>-66)&(ds.nav_lat_grid_T<-64)).mean(dim={'x','y'})
ds_wilson.to_netcdf(f'./clim_wilson_EXP_{exp}.nc')





