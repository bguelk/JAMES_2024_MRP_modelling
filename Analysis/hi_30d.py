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
ds16=xr.open_dataset(f'./hi800_2016_EXP_{exp}.nc')
ds16.coords['year']=ds16.t.dt.year
ds16.coords['month']=ds16.t.dt.month

ds17=xr.open_dataset(f'./hi800_2017_EXP_{exp}.nc')
ds17.coords['year']=ds17.t.dt.year
ds17.coords['month']=ds17.t.dt.month

bat=xr.open_dataset('../1_domain_cfg_50levels_new.nc')
bat.coords['nav_lon']=bat.nav_lon
bat.coords['nav_lat']=bat.nav_lat

dt=30

ds16.hi.isel(t=slice(198-dt,198)).to_netcdf(f'./hi800_prepolynya_{exp}_2016.nc')
ds17.hi.isel(t=slice(180-dt,180)).to_netcdf(f'./hi800_prepolynya_{exp}_2017.nc')
