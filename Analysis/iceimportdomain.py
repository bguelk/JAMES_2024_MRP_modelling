#!/usr/bin/env python
# coding: utf-8
import numpy as np
import xarray as xr
import xnemogcm 
import xgcm
import sys
from pathlib import Path
exp=sys.argv[1]

path_in=Path('./')

xr.set_options(keep_attrs=True)
ds = xnemogcm.open_nemo_and_domain_cfg(nemo_files=list(path_in.glob('./Maud12t_20*.nc')), domcfg_files=['../1_domain_cfg_50levels_new.nc'],nemo_kwargs=dict(datadir='./'))

ds['bathy_meter']=ds.bathy_meter.swap_dims({'x':'x_c','y':'y_c'})
ds['x_c'].attrs['axis'] = 'X'
ds['y_c'].attrs['axis'] = 'Y'
ds = ds.drop_vars('ncatice', errors='ignore')
# ice velocity is on the U/ V Grid points
# this is corrected here: 
ds['sivelu']=ds.sivelu.swap_dims({'x_c':'x_f'})
ds['sivelv']=ds.sivelv.swap_dims({'y_c':'y_f'})

metrics = {
   ('X',): ['e1t', 'e1u', 'e1v', 'e1f'], # X distances
   ('Y',): ['e2t', 'e2u', 'e2v', 'e2f'], # Y distances
}
grid = xgcm.Grid(ds, metrics=metrics, periodic=False)


# zonal advection of ice: ice volume ( concentration *thickness) * ui* e2u  [m *m/s*m =m^3/s]
ice_adv_u= ds.sivelu*ds.e2u*grid.interp(ds.sivolu,'X',boundary='extend')
# meridional advection of ice: ice volume ( concentration *thickness) * vi* e1v  [m *m/s*m =m^3/s]
ice_adv_v= ds.sivelv*ds.e1v*grid.interp(ds.sivolu,'Y',boundary='extend')

# now we want the transport from the boundaries to the center of the domain. There are 4 grid points representing the boundary
# for the eastern and western boundary we want the data from the x_f=3.5 and x_f=290.5, y_c=0 and y_c=266
# for the northern boundary : y_f=265.5 , x_c=4 and x_c=291 (southern boundary is land and not forced)

#eastern boundary
iceadv_eb=ice_adv_u.isel(x_f=290,y_c=slice(0,266)).sum(dim='y_c')
#western boundary
iceadv_wb=ice_adv_u.isel(x_f=3,y_c=slice(0,266)).sum(dim='y_c')
#northern boundary
iceadv_nb=ice_adv_v.isel(x_c=slice(4,291),y_f=265).sum(dim='x_c')

iceadv_eb.assign_attrs(long_name='Ice Volume across the eastern boundary')
iceadv_eb=iceadv_eb.rename("iceadv_eb")
iceadv_eb.to_netcdf(f'./iceadv_eb_EXP_{exp}.nc')

iceadv_wb.assign_attrs(long_name='Ice Volume across the western boundary')
iceadv_wb=iceadv_wb.rename("iceadv_wb")
iceadv_wb.to_netcdf(f'./iceadv_wb_EXP_{exp}.nc')

iceadv_nb.assign_attrs(long_name='Ice Volume across the northern boundary')
iceadv_nb=iceadv_nb.rename("iceadv_nb")
iceadv_nb.to_netcdf(f'./iceadv_nb_EXP_{exp}.nc')
