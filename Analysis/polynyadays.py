#!/usr/bin/env python
# coding: utf-8
import numpy as np
import xarray as xr
from pathlib import Path
xr.set_options(keep_attrs=True)
dim_3D = ("y","x","year")
dim_2D = ("y","x")
# import experiment name from bash script
import sys
exp=sys.argv[1]

ds= xr.open_mfdataset('../MAUD12_1d_20120101_20180110_icemod.nc')
ds.coords['year']=ds.time_counter.dt.year
ds.coords['month']=ds.time_counter.dt.month
siv_03=np.zeros((len(ds.y),len(ds.x),6))
siv_01=np.zeros((len(ds.y),len(ds.x),6))
sic_06=np.zeros((len(ds.y),len(ds.x),6))
sic_04=np.zeros((len(ds.y),len(ds.x),6))
sic_02=np.zeros((len(ds.y),len(ds.x),6))


i=0
for y in range(2012,2018):
    # count days where the Sea ice volumne was lower than 0.3 m and 0.1m
    siv_03[:,:,i]=xr.where(ds.sivolu.where((ds.year==y)&(ds.month>6)&(ds.month<10))<0.3,1,0).sum(dim="time_counter")
    siv_01[:,:,i]=xr.where(ds.sivolu.where((ds.year==y)&(ds.month>6)&(ds.month<10))<0.1,1,0).sum(dim="time_counter")
    # count days  where the SIC was lower than 0.6; 0.4; 0.2
    sic_06[:,:,i]=xr.where(ds.siconc.where((ds.year==y)&(ds.month>6)&(ds.month<10))<0.6,1,0).sum(dim="time_counter")
    sic_04[:,:,i]=xr.where(ds.siconc.where((ds.year==y)&(ds.month>6)&(ds.month<10))<0.4,1,0).sum(dim="time_counter")
    sic_02[:,:,i]=xr.where(ds.siconc.where((ds.year==y)&(ds.month>6)&(ds.month<10))<0.2,1,0).sum(dim="time_counter")
    i=i+1

ds_dc= xr.Dataset(
    data_vars=dict(
              siv_03=(dim_3D, siv_03.data),
              siv_01=(dim_3D, siv_01.data),
              sic_06=(dim_3D, sic_06.data),
              sic_04=(dim_3D, sic_04.data),
              sic_02=(dim_3D, sic_02.data)
              ),
    coords=dict(
              x=(["x"],ds.x.data),
              y=(["y"],ds.y.data),
              year=(["year"],np.arange(2012,2018))
              )
)

ds_dc = ds_dc.assign_coords({
     "lat": (["y", "x"],ds.nav_lat.data),
     "lon": (["y", "x"],ds.nav_lon.data)
})

ds_dc.to_netcdf(f'./polynyacount_EXP_{exp}.nc')
