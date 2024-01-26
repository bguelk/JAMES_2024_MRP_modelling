#!/usr/bin/env pyton
# coding: utf-8
import numpy as np
import xarray as xr
from pathlib import Path
import cmocean.cm as cmo
import matplotlib.pyplot as plt
from skimage.morphology import dilation
from skimage.morphology import disk
xr.set_options(keep_attrs=True)

# import experiment name from bash script
exp='tpre02_prsn02_2012'#sys.argv[1]
path_in=Path('./')
year=2016

ds=xr.open_mfdataset(f'./Maud12t_{year}_grid_[T,W].nc')
bat=xr.open_dataset('../1_domain_cfg_50levels_new.nc')
bat.coords['nav_lon']=bat.nav_lon
bat.coords['nav_lat']=bat.nav_lat

ds=xr.merge((ds,bat))
ds['mask_tc']=np.zeros((len(ds.y),len(ds.x)))*(ds.bathy_meter.where(ds.bathy_meter<2500))+1
ds['mask_tc']=ds.mask_tc.where(((ds.mask_tc==1)&(ds.glamt<4.3)&(ds.glamt>0.5)&(ds.gphit>-65.5)),other=0)
mask_tc=ds.mask_tc
mask_tc[173,98]=1
mask_tc[178,109]=0
ds['mask_tc']=mask_tc
# mask_ha_all refers to region of the flanks
mean_bathy = ds.bathy_meter.rolling(x=13,center=True).mean().rolling(y=13,center=True).mean()
ds['mask_tr_all']=np.zeros((len(ds.y),len(ds.x)))*(mean_bathy.where(mean_bathy<3500))+1
ds['mask_tr_all']=ds.mask_tr_all.where(((ds.mask_tr_all==1)&(ds.glamt<8)&(ds.gphit>-66.5)),other=0)
ds['mask_tr']=ds.mask_tr_all-ds.mask_tc
mask_tr=ds.mask_tr

ds['mask_ha'] = xr.DataArray(dilation(ds.mask_tr_all, disk(14)) - ds.mask_tr_all,dims=('y', 'x'))
ds['mask_ha_all'] = ds.mask_ha+ds.mask_tr_all
mask_ha=ds.mask_ha



ds=ds.where((ds.nav_lon>-2)&(ds.nav_lon<10)&(ds.nav_lat>-67)&(ds.nav_lat<-63),drop=True)
ds.coords['year']=ds.time_counter.dt.year
ds.coords['month']=ds.time_counter.dt.month
# mask by 50m below MLD
ds["n2_blwmld50"]=ds.bn2.where(ds.depthw>(ds.mldr10_1+50))

# separate in seasons
ds["n2_wi50"]=ds.n2_blwmld50.where((ds.month>6)&(ds.month<10),drop=True)
ds["n2_su50"]=ds.n2_blwmld50.where((ds.month<4),drop=True)
ds["n2_au50"]=ds.n2_blwmld50.where((ds.month>3)&(ds.month<7),drop=True)
ds["n2_sp50"]=ds.n2_blwmld50.where((ds.month>9),drop=True)

ds.n2_wi50.where((ds.month>6)&(ds.month<10),drop=True).to_netcdf(f'./n2_wi50_{exp}_{year}.nc')
ds.n2_su50.where((ds.month<4),drop=True).to_netcdf(f'./n2_su50_{exp}_{year}.nc')
ds.n2_au50.where((ds.month>3)&(ds.month<7),drop=True).to_netcdf(f'./n2_au50_{exp}_{year}.nc')
ds.n2_sp50.where((ds.month>9),drop=True).to_netcdf(f'./n2_sp50_{exp}_{year}.nc')

