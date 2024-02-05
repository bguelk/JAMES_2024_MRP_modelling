# Maud12 configuration

Maud12 is a regional NEMO configurations, developed with NEMO 4.2.0 Maud12 is set up in the region of Maud Rise in the Weddell Sea, with the domain covering 5°W to 19.5°E and 70.5°S to 61.5°S.

Technical details:
- horizontal resolution: 1/12°
- vertical levels: 50
- grid: Mercator grid; same grid points as GLORYS12
- bathymetry: GEBCO
- inital state of temperature, salinity and sea ice: GLORYS12
- lateral forcing: GLORYS12
- surface forcing: JRA55-do version 1.5

An example namelist_cfg and namelist_ice_cfg can be found below.
Between the different simulations either ln_zdfevd for EVD or ln_zdfmfc for EDMF is varied. Further, different files for sn_prec and sn_snow are provided, depending on the surface forcing.



The modified EDMF rountines can be found in EDMF_routines. These routines need to be copied into the MY_SRC of the configuration and renamed  to "zdfmfc.F90" before compilation.