#!/usr/bin/env python
# coding: utf-8
import numpy as np
import xarray as xr
from pathlib import Path
import cmocean.cm as cmo
import matplotlib.pyplot as plt
from skimage.morphology import dilation
from skimage.morphology import disk
xr.set_options(keep_attrs=True)

dim_2D = ("y","x")
dim_3D = ("t","y","x")
# import experiment name from bash script
import sys
exp=sys.argv[1]
path_in=Path('./')
year=2016

bat=xr.open_dataset('../1_domain_cfg_50levels_new.nc')
bat.coords['nav_lon']=bat.nav_lon
bat.coords['nav_lat']=bat.nav_lat
# now split the domain in different regions 
# The Taylor Column with a shallower than 2500m Bathymetry,
# the Transition Zone between 2500 m and 3500 m Depth
# the Halo, 14 grid points outside of the Transition Zone
bat['mask_tc']=np.zeros((len(bat.y),len(bat.x)))*(bat.bathy_meter.where(bat.bathy_meter<2500))+1
bat['mask_tc']=bat.mask_tc.where(((bat.mask_tc==1)&(bat.glamt<4.3)&(bat.glamt>0.5)&(bat.gphit>-65.5)),other=0)
mask_tc=bat.mask_tc
mask_tc[173,98]=1
mask_tc[178,109]=0
bat['mask_tc']=mask_tc
mean_bathy = bat.bathy_meter.rolling(x=13,center=True).mean().rolling(y=13,center=True).mean()
bat['mask_tr_all']=np.zeros((len(bat.y),len(bat.x)))*(mean_bathy.where(mean_bathy<3500))+1
bat['mask_tr_all']=bat.mask_tr_all.where(((bat.mask_tr_all==1)&(bat.glamt<8)&(bat.gphit>-66.5)),other=0)
bat['mask_tr']=bat.mask_tr_all-bat.mask_tc
mask_tr=bat.mask_tr

bat['mask_ha'] = xr.DataArray(dilation(bat.mask_tr_all, disk(14)) - bat.mask_tr_all,dims=('y', 'x'))
bat['mask_ha_all'] = bat.mask_ha+bat.mask_tr_all


ds=xr.open_mfdataset(f'./Maud12t_{year}_grid_[T,W].nc')

wp_blwmld50=xr.where(ds.mf_wp.where(ds.depthw>(ds.mldr10_1+50))>0,1,0)
#focus on MLD:..
dim_4D = ("t","depthw","y","x")

ds_dc=xr.Dataset(
      data_vars=dict(wp_blwmld50=(dim_4D,wp_blwmld50.data)),
      coords=dict(depthw=(["depthw"],ds.depthw.data),
                 x=(["x"],ds.x.data),
                 y=(["y"],ds.y.data),
                 t=(["t"],ds.time_counter.data )
       ))
ds_dc = ds_dc.assign_coords({
     "lat": (["y", "x"],ds.nav_lat.data),
     "lon": (["y", "x"],ds.nav_lon.data)})

ds_dc.to_netcdf(f'./mfwp_propertiesblwmld50_{year}_{exp}.nc')




#focus on regions...

ds=xr.open_dataset(f'./mfwp_propertiesblwmld50_{year}_{exp}.nc')
ds.coords['year']=ds.t.dt.year
ds.coords['month']=ds.t.dt.month
ds=xr.merge((ds,bat))

wp_wi50=ds.wp_blwmld50.where((ds.month>6)&(ds.month<10))
wp_su50=ds.wp_blwmld50.where((ds.month<4))
wp_au50=ds.wp_blwmld50.where((ds.month>3)&(ds.month<7))
wp_sp50=ds.wp_blwmld50.where((ds.month>9))

dim_2D = ("depthw","y","x")

ds_dc= xr.Dataset(
      data_vars=dict(wp_su50=(dim_2D,wp_su50.sum(dim={'t'}).data),
                     wp_wi50=(dim_2D,wp_wi50.sum(dim={'t'}).data),
                     wp_au50=(dim_2D,wp_au50.sum(dim={'t'}).data),
                     wp_sp50=(dim_2D,wp_sp50.sum(dim={'t'}).data)),
     coords=dict(depthw=(["depthw"],ds.depthw.data),
                 x=(["x"],ds.x.data),
                 y=(["y"],ds.y.data)
                  )
       )

ds_dc = ds_dc.assign_coords({
     "lat": (["y", "x"],ds.nav_lat.data),
     "lon": (["y", "x"],ds.nav_lon.data)})
ds_dc["year"]=ds.year.isel(t=0).values
ds_dc=ds_dc.expand_dims(dim="year")
ds_dc.to_netcdf(f'./mfwp_propertiesblwmld50_seas_{year}_{exp}.nc')
