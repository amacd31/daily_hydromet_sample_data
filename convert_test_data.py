import pandas as pd

# Read and convert flow column (79623_00060) to cubic meters per second (by * 0.0283168)
cumecs = pd.read_csv(
    'usgs_02430680_original.csv.gz',
    sep='\t', # Tab separated
    skiprows=33, # 33 rows of header
    index_col='datetime',
    parse_dates=True,
    low_memory=False
)['79623_00060'] * 0.0283168

# Convert from cumecs to average ML/day
ml_per_day = cumecs.resample('D').mean() * 86.4

ml_per_day.to_csv('USGS_02430680_streamflow.csv')
