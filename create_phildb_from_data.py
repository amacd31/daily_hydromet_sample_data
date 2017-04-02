import iris
import numpy as np
import os
import pandas as pd
import sys

from iris.pandas import as_data_frame
from phildb.create import create
from phildb.database import PhilDB
from phildb.exceptions import AlreadyExistsError, DuplicateError

iris.FUTURE.netcdf_promote = True

if len(sys.argv) < 2:
    print("Require path to folder with precip netcdf files.")
    exit(1)

data_dir = sys.argv[1]

db_name = 'cpc_unified_precipitation'

try:
    create(db_name)
except AlreadyExistsError:
    pass

db = PhilDB(db_name)

#################### PRECIPITATION ############################
try:
    db.add_source('NOAA', 'NOAA')
except DuplicateError:
    pass

try:
    db.add_measurand('P', 'PRECIPITATION', 'Precipitation')
except DuplicateError:
    pass

try:
    db.add_timeseries('USGS_02430680')
except DuplicateError:
    pass

try:
    db.add_timeseries_instance('USGS_02430680', 'D', 'CPC Unified Gauge-Based Analysis of Daily Precipitation over CONUS', measurand = 'P', source = 'NOAA')
except DuplicateError:
    pass

for year in range(1983, 2007):
    cube = iris.load_cube(os.path.join(data_dir, 'precip.V1.0.{0}.nc'.format(year)))

    catchment_rainfall = cube.extract(iris.Constraint(longitude=lambda cell: 271.375 <= cell <= 271.375, latitude=lambda cell: 34.375 <= cell <= 34.625))

    catchment_average = as_data_frame(catchment_rainfall).mean(axis=1)

    db.write('USGS_02430680', 'D', catchment_average, measurand = 'P', source = 'NOAA')

#################### STREAMFLOW ############################
try:
    db.add_measurand('Q', 'STREAMFLOW', 'Streamflow')
except DuplicateError:
    pass

try:
    db.add_source('USGS', 'U.S. Geological Survey')
except DuplicateError:
    pass

try:
    db.add_timeseries_instance('USGS_02430680', 'D', 'USGS 02430680 TWENTYMILE CREEK NR GUNTOWN, MS', measurand = 'Q', source = 'USGS')
except DuplicateError:
    pass

streamflow = pd.read_csv('usgs_02430680_streamflow.csv', parse_dates=True, index_col=0, header=None)
db.write('USGS_02430680', 'D', streamflow, measurand = 'Q', source = 'USGS')

#################### PET ############################

try:
    db.add_timeseries('2431000')
except DuplicateError:
    pass

try:
    db.add_measurand('PET', 'POTENTIAL_EVAPOTRANSPIRATION', 'Potential Evapotranspiration')
except DuplicateError:
    pass

try:
    db.add_source('ORNL_DAAC', 'ORNL DAAC, Oak Ridge, Tennessee, USA')
except DuplicateError:
    pass

try:
    db.add_timeseries_instance('2431000', 'D', 'TOMBIGBEE RIVER NR FULTON, MS; disaggregated monthly series', measurand = 'PET', source = 'ORNL_DAAC')
except DuplicateError:
    pass

from calendar import monthrange
monthly_pet = pd.Series(pd.read_csv('2431000.pet', sep='\s+', header = None).mean()[2:].values, pd.date_range('2000-01-01', periods = 12, freq='MS'), name='date')
df = pd.DataFrame({'ts': monthly_pet}).reset_index()
df.columns = ['date', 'ts']
df['ndays'] = df.date.apply(lambda x: monthrange(x.year,x.month)[1])
df.set_index('date', inplace=True)
pet_daily_climatology = df.eval('ts / ndays').resample('D').interpolate()
pet_daily_climatology = pet_daily_climatology.append(pd.Series(pet_daily_climatology.ix['2000-01-01'], index = [pd.to_datetime('2000-12-31')])).resample('D').interpolate()

non_leap_pet = pet_daily_climatology.ix[pet_daily_climatology.index != pd.to_datetime('2000-02-29')]
daily_pet = pd.Series()
for year in streamflow.asfreq('AS').index.year:
    idx = pd.date_range('{0}-01-01'.format(year), '{0}-12-31'.format(year), freq='D')
    if monthrange(year, 2)[1] == 29:
        daily_pet = daily_pet.append(pd.Series(pet_daily_climatology.values, idx))
    else:
        daily_pet = daily_pet.append(pd.Series(non_leap_pet.values, idx))

db.write('2431000', 'D', daily_pet, measurand = 'PET', source = 'ORNL_DAAC')
