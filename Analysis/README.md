# Content
- Analysis for several experiments:
    - iceimportdomain.py:
    This script computes the import of ice across the boundaries into the model domain. The data is then used by boundaries_ice.ipynb
    - boundaries_ice.ipynb:
    This script computes the total freshening rate $\Delta S_ice$ for Table 1
    - freshwaterbudget.py:
    This script computes the freshwater content according to Equation 7.
    - freshwaterbudget.ipynb:
    This script estimates the trend of the freshwater content for Table 1 and Table S1
    - climatology.py:
    This script extracts from a mulityear-monthly mean the region as indicated in Figure 1 for Figure 2 
    - n2_violin.py:
    This script is extratcing the values of N^2 for a given year below 50m below the MLD for the Taylor Cap and the Flanks of Maud Rise. The extracted data is used for Figure 9.
    - mfwp_properties.py:
    This script is masking grid cells if they are larger/smaller than 0 and then extracted for the Taylor Cap and the Flanks of Maud Rise. The data is later used for Figure 10.
    - polynyadays.py:
    This script extracts the number of days between July and September, where a threshold in sea ice concentration/volume is reached. Parts of the data is visualized in Figure 3
    - polynya_area.py:
    This script computes the area below a certain SIC threshold, as visualized in Figure 4
    - saltdeficit.py:
    This script computes the salt deficit following Equation 8
    - hi_30d.py:
    Extracts the salt deficit of the 30days before deep convection as visulaized in Figure 7
    - convectiveresistance.py:
    This script computes the convective resistance following Equation 9
    - deepconvection.py:
    This script applies a mask of deep convective cells (MLD >830) or not
    - plume_beforedc.py:
    This script extracts the plume velocity in the 30days before deep convection as visualized in Figure 7
    - saltadvection.py:
    This script computes the saltanomaly in the period before the onset of deep convection in 2016 and 2017 as visualized in Figure 7