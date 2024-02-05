#!/usr/bin/env python
# coding: utf-8
import numpy as np
import xarray as xr
from pathlib import Path
xr.set_options(keep_attrs=True)

dim_2D = ("y","x")
# import experiment name from bash script
import sys
exp=sys.argv[1]


for year in range(2012,2018):
    print(year)
    ds= xr.open_mfdataset(f'./Maud12t_{year}_grid_T.nc')
    # count where the MLD was deeper than 200 m
    dc_200=xr.where(ds.mldr10_1>200,1,0).sum(dim="time_counter")
    # count where the MLD was deeper than 500 m
    dc_500=xr.where(ds.mldr10_1>500,1,0).sum(dim="time_counter")
    dc_800=xr.where(ds.mldr10_1>800,1,0).sum(dim="time_counter")
    dc_830=xr.where(ds.mldr10_1>830,1,0).sum(dim="time_counter")
    ds_dc= xr.Dataset(
        data_vars=dict(
                  dc_200=(dim_2D, dc_200.data),
                  dc_500=(dim_2D, dc_500.data),
                  dc_800=(dim_2D, dc_800.data),
                  dc_830=(dim_2D, dc_830.data)),
         coords=dict(
                  x=(["x"],ds.x.data),
                  y=(["y"],ds.y.data),
                  )
        )
    ds_dc.coords['year']=year
    ds_dc = ds_dc.expand_dims(dim={'year':1})
    ds_dc = ds_dc.assign_coords({
        "lat": (["y", "x"],ds.nav_lat_grid_T.data),
        "lon": (["y", "x"],ds.nav_lon_grid_T.data)
    })
    ds_dc.to_netcdf(f'./dc_count_{year}_EXP_{exp}.nc')
