from socket import if_nameindex
from urllib.request import urlretrieve
import os


#output_relative_dir = '../data/raw/'

#YEARS = range(2017, 2020)
#MONTHS = range(6, 9)


URL_TEMPLATE = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_"#year-month.parquet
URL_TEMPLATE_GREEN = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_"#year-month.parquet
URL_TEMPLATE_FHV = "https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_"#year-month.parquet


def do_download(template, dir, years, months):
    if not os.path.exists(dir):
        os.makedirs(dir)
    for year in years:
        # data output directory is `data
        tlc_output_dir = dir

        for month in months:
            # 0-fill i.e 1 -> 01, 2 -> 02, etc
            month = str(month).zfill(2) 
            print(f"Begin month {year}.{month}")
            
            # generate url for yellow
            url = f'{template}{year}-{month}.parquet'
            # generate output location and filename
            output_dir = f"{tlc_output_dir}/{year}_{month}.parquet"
            print(output_dir)
            # download
            urlretrieve(url, output_dir) 
            print(f"Completed month {month}-{year}")

do_download(URL_TEMPLATE, '../data/raw/yellow', range(2017, 2020), range(6, 9))
do_download(URL_TEMPLATE_GREEN, '../data/raw/green', range(2017, 2020), range(6, 9))
do_download(URL_TEMPLATE_FHV, '../data/raw/fhv', range(2017, 2020), range(6, 9))

#print("Begin beach.csv")
#urlretrieve("https://data.cityofnewyork.us/api/views/fxgv-ba35/rows.csv?accessType=DOWNLOAD", f"{output_relative_dir}/beach.csv")
