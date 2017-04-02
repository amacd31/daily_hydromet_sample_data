import pandas as pd
from phildb.database import PhilDB

db = PhilDB('cpc_unified_precipitation')

sf = db.read('USGS_02430680', 'D', measurand = 'Q').dropna().asfreq('D')
p = db.read('USGS_02430680', 'D', measurand = 'P').dropna().asfreq('D')
pet = db.read('2431000', 'D', measurand = 'PET')

df = pd.DataFrame({'P': p, 'Q': sf, 'PE': pet})
df.asfreq('D').ix['1988':'2006-12-31'].to_csv('USGS_02430680_combined.csv')
