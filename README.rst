Public domain daily hydro-meterological dataset
===============================================

This repository contains streamflow, precipitation, and
potential-evapotranspiration data for the Twentymile Creek USGS streamflow
station. The purpose of this repository is to provide a readily reused dataset
for hydrological modelling tests.

USGS_02430680_combined.csv
--------------------------
USGS_02430680_combined.csv is the core file with the derived dataset of
streamflow, precipitation and potential evapotranspiration. All the other files
are either supporting data files or scripts used in producing this file.

This file is produced using the make_combined_csv.py script once the cpc_unified_precipitation PhilDB database has been populated using create_phildb_from_data.py.

USGS_02430680_streamflow.csv
----------------------------
Streamflow station: https://waterdata.usgs.gov/ms/nwis/uv?site_no=02430680

Derived from originally downloaded data: usgs_02430680_original.csv.gz using convert_test_data.py

USGS_02430680.json
------------------
Catchment boundary USGS_02430680.json derived from:
    Viger, Roland J. and Bock, Andrew, 2014, GIS Features of the Geospatial Fabric for National Hydrologic Modeling, US Geological Survey, http://dx.doi.org/doi:10.5066/F7542KMD.
    Roland J. Viger, 2014, Preliminary spatial parameters for PRMS based on the Geospatial Fabric, NLCD2001 and SSURGO, US Geological Survey, http://dx.doi.org/doi:10.5066/F7WM1BF7.

The upstream catchment area was selected and extracted using QGIS.

USGS_02430680_grid.csv
----------------------
Grid points that the catchment boundary overlaps in the CPC US Unified
Precipitation grids. Selected using get_grid_cells in:
https://github.com/amacd31/catchment_tools/blob/f02b56b/catchment_tools/catchment_cutter.py

USGS_02430680.area
------------------
The catchment size was calculated from the geojson data and stored in
USGS_02430680.area (using the get_area method in:
https://github.com/amacd31/hydromet-toolkit/blob/c9596e0f5d1807a10df3f0b9f976048ebcc4b691/hydromet/catchments.py)

2431000.pet
-----------
PET data from ORNL:
    Vogel, R.M., and A. Sankarasubramanian. 2015. Monthly Climate Data for Selected USGS HCDN Sites, 1951-1990, R1. ORNL DAAC, Oak Ridge, Tennessee, USA. http://dx.doi.org/10.3334/ORNLDAAC/810

The PET data at station 2431000 "TOMBIGBEE RIVER NR FULTON, MS" was the nearest
PET station to 02430680. The monthly PET data was dis-aggregated into the
PhilDB instance with the create_phildb_from_data.py script before the combined
csv file was produce.

create_phildb_from_data.py
--------------------------
Creates a PhilDB database processing the CPC US Unified Precipitation grid data
into a precipitation series, loads the streamflow CSV data into the database,
and dis-aggregates the potential evapotranspiration data into daily data before
loading.
