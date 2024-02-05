#!/usr/bin/env python
# coding: utf-8
import numpy as np
import xarray as xr
from pathlib import Path
import cmocean.cm as cmo
import matplotlib.pyplot as plt
xr.set_options(keep_attrs=True)

dim_2D = ("y","x")
dim_3D = ("t","y","x")
# import experiment name from bash script
import sys
exp=sys.argv[1]
path_in=Path('./')
#heat capacity of seawater
dsm16=xr.open_mfdataset('./mld_2016.nc')
ds16=xr.open_dataset('./Maud12t_2016_grid_W.nc')
ds16.coords['year']=ds16.time_counter.dt.year
ds16.coords['month']=ds16.time_counter.dt.month

dsm17=xr.open_mfdataset('./mld_2017.nc')
ds17=xr.open_dataset('./Maud12t_2017_grid_W.nc')
ds17.coords['year']=ds17.time_counter.dt.year
ds17.coords['month']=ds17.time_counter.dt.month

bat=xr.open_dataset('../1_domain_cfg_50levels_new.nc')
bat.coords['nav_lon']=bat.nav_lon
bat.coords['nav_lat']=bat.nav_lat
# check out maps of plume velocity before the deep convection event 
#2016, first time MLD>800m 17.07.2016 (time_counter=198)



ds16.mf_wp.where((ds16.nav_lon>1.5)&(ds16.nav_lon<5)&(ds16.nav_lat<-63.9)&(ds16.nav_lat>-64.3),drop=True).to_netcdf(f'./wp_dcreg_2016_{exp}.nc')

ds17.mf_wp.where((ds17.nav_lon>5.3)&(ds17.nav_lon<5.9)&(ds17.nav_lat<-64.2)&(ds17.nav_lat>-64.6),drop=True).to_netcdf(f'./wp_dcreg_2017_{exp}.nc')
