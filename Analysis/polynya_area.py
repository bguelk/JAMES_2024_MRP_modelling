#!/usr/bin/env python
# coding: utf-8
import numpy as np
import xarray as xr
from pathlib import Path
import xnemogcm 
import xgcm
xr.set_options(keep_attrs=True)
dim_3D = ("t","y","x")
dim_1D = ("t")
path_in=Path('./')
# import experiment name from bash script
year=2017
exp=sys.arg[1]
ds = xnemogcm.open_nemo_and_domain_cfg(nemo_files=list(path_in.glob(f'Maud12t_{year}*.nc')), domcfg_files=['../1_domain_cfg_50levels_new.nc'],nemo_kwargs=dict(datadir='./',chunks={'time_counter':1}))
ds['bathy_meter']=ds.bathy_meter.swap_dims({'x':'x_c','y':'y_c'})
ds['x_c'].attrs['axis'] = 'X'
ds['y_c'].attrs['axis'] = 'Y'
ds['month']=ds.t.dt.month

metrics = {
   ('X',): ['e1t', 'e1u', 'e1v', 'e1f'], # X distances
   ('Y',): ['e2t', 'e2u', 'e2v', 'e2f'], # Y distances
}
grid = xgcm.Grid(ds, metrics=metrics, periodic=False)


sic50=xr.where(ds.siconc.where((ds.nav_lon_grid_T>-4)&(ds.nav_lon_grid_T<10)&(ds.nav_lat_grid_T>-67)&(ds.nav_lat_grid_T<-62))<0.5,1,0)

pa_50= grid.integrate(sic50,['X','Y'])


sic10=xr.where(ds.siconc.where((ds.nav_lon_grid_T>-4)&(ds.nav_lon_grid_T<10)&(ds.nav_lat_grid_T>-67)&(ds.nav_lat_grid_T<-62))<0.1,1,0)

pa_10= grid.integrate(sic10,['X','Y'])




ds_dc= xr.Dataset(
    data_vars=dict(
              sic50 = (dim_3D, sic50.data),
              sic10 = (dim_3D, sic10.data),
              pa_50 = (dim_1D, pa_50.data),
              pa_10 = (dim_1D, pa_10.data)
              ),
    coords=dict(
              x=(["x"],ds.x.data),
              y=(["y"],ds.y.data),
              t=(["t"],ds.t.data)
              )
)

ds_dc = ds_dc.assign_coords({
     "lat": (["y", "x"],ds.nav_lat_grid_T.data),
     "lon": (["y", "x"],ds.nav_lon_grid_T.data)
})

ds_dc.to_netcdf(f'./polynya_area_{year}_EXP_{exp}.nc')
