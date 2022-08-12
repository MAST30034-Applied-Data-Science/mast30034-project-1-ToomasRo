from urllib.request import urlretrieve
import os


output_relative_dir = '../data/raw'
target_dir = ''
YEARS = ['2019', '2020']
MONTHS = range(1, 2)

for year in YEARS:
    if not os.path.exists(output_relative_dir + target_dir + year):
        os.makedirs(output_relative_dir + target_dir + year)

URL_TEMPLATE = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_"#year-month.parquet

for year in YEARS:

    # data output directory is `data
    tlc_output_dir = output_relative_dir

    for month in MONTHS:
        # 0-fill i.e 1 -> 01, 2 -> 02, etc
        month = str(month).zfill(2) 
        print(f"Begin month {year}.{month}")
        
        # generate url
        url = f'{URL_TEMPLATE}{year}-{month}.parquet'
        # generate output location and filename
        output_dir = f"{tlc_output_dir}/{year}_{month}.parquet"
        print(output_dir)
        break
        # download
        urlretrieve(url, output_dir) 
        
        print(f"Completed month {month}")