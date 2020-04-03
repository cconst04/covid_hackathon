from random import random,randint
import pandas as pd
from datetime import datetime,timedelta
lat_range = (34.824426,34.924698)
lon_range = (33.278905,33.166295)
fines_range = (10,100)
total_records = 10
date_range = 10
lat_diff = lat_range[1]-lat_range[0]
lon_diff = lon_range[1]-lon_range[0]
out_data = {
    'date':[],
	'count': [],
    'lat': [],
    'lon': []
}
for i in range(total_records):
    lat = lat_range[0]+random()*lat_diff
    lon = lon_range[0]+random()*lon_diff
    out_data['count'].append(randint(fines_range[0],fines_range[1]))
    out_data['lat'].append(lat)
    out_data['lon'].append(lon)
    out_data['date'].append(datetime.now()-timedelta(days=randint(0,date_range)))

records = pd.DataFrame(out_data,columns=['date','lat','lon','count'])
records.to_csv ('fines.csv', index = False, header=True)
