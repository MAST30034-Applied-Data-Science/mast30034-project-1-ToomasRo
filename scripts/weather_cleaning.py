import pandas as pd
import numpy as np
import os

TEMP_DIR = '../data/temp/weather'

def clean(years):
   
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    

    for year in years:
        print(year)
        df = pd.read_csv(f'../data/raw/weather/{year}_weather.csv')

        df.rename(str.lower, axis='columns', inplace=True)
        df = df[df.report_type.isin(['FM-12', 'FM-15', 'FM-16'])]
        df.drop('report_type', axis=1, inplace=True)
        df.head()

        # keeping potentially relevant columns
        df = df[['date', 'wnd', 'vis', 'tmp', 'dew', 'slp', 'ga1', ]]
        if True:
            # loosely transcribed meaning of columns:

            # wnd = wind angle clockwise,  quality code, wind obs type, WIND-OBSERVATION speed rate (x10), quality # 9999 missing

            # vis = visibility distance, quality, variability, obs qual  # 999999=missing

            # tmp = temp (x10), #+9999=missing
            # dew = dewpoint(x10), #+9999=missing [dew point temperature The temperature to which a given parcel of air must be cooled at constant pressure and water vapor content in order for saturation to occur

            # slp = atm pressure (x10), # 99999 = missing           [seal level pressure]
            # ga1 = cloud cover (scale 0-8, 9&10=obstructed), quality, base height, quality, cloud type, quality

            # Maybe interesting columns:
            # mw1 = weather name, quality
            # oc1 = kui suured tuulepuhangud on (x10), quality

            # df.drop(['source', 'station', 'latitude', 'longitude', 'name', 'elevation', 'call_sign', 'quality_control', 'cig', 'aa1', 'aa2', 'aa3', 'ab1', 'ad1', 'ae1', 'ah1', 'ah2', 'ah3', 'ah4', 'ah5', 'ah6', 'ai1', 'ai2', 'ai3', 'ai4', 'ai5', 'ai6', 'aj1', 'ak1', 'al1', 'am1', 'an1', 'at1', 'at2', 'at3', 'at4', 'at5', 'at6', 'at7', 'at8', 'au1', 'au2', 'au3', 'au4', 'aw1', 'aw2', 'aw3', 'aw4', 'aw5','ax1', 'ax2', 'ax3', 'ax4', 'ed1', 'ga2', 'ga3', 'gd1', 'gd2', 'gd3', 'gd4', 'ge1', 'gf1', 'ka1', 'ka2', 'kb1','kb2','kb3','kc1','kc2','kd1','kd2','ke1','kg1','kg2','ma1','md1', 'mf1','mg1','mh1','mk1','mv1','mw1','mw2','mw3','oc1','od1','oe1','oe2','oe3','rh1','rh2','rh3','rem','eqd'], axis=1)
            # spliting out the relevant information
            ...
        df['date'] = df['date'] = pd.to_datetime(df['date'])
        df['wnd'] = df['wnd'].str.split(',', expand=True)[3].astype(
            np.uint32)      # unit: m/s, scaling factor:10,     missing: 9999
        df['vis'] = df['vis'].str.split(',', expand=True)[
            0].astype(np.uint32)      # unit: m,
        df['tmp'] = df['tmp'].str.split(',', expand=True)[0].astype(
            np.int32)       # unit: C, scaling factor:10,       missing: 9999
        df['dew'] = df['dew'].str.split(',', expand=True)[0].astype(
            np.int32)       # unit: C, scaling factor:10,       missing: 9999
        df['atm'] = df['slp'].str.split(',', expand=True)[0].astype(
            np.uint32)      # unit: hP, scaling factor:10,      missing: 99999
        df['ga1'].fillna('99,x', inplace=True)
        df['cc'] = df['ga1'].str.split(',', expand=True)[0].astype(np.uint32).astype(
            'category')  # cloud coverage: unit: okta (0 clear -> 8 covered), 99 missing
        df.drop(['slp', 'ga1'], axis=1, inplace=True)
        df = df[(df['wnd'] != 9999)]
        df = df[(df['vis'] != 999999)]
        df = df[(df['tmp'] != 9999)]
        df = df[(df['dew'] != 9999)]
        df = df[(df['atm'] != 99999)]

        df.to_csv(f'{TEMP_DIR}/{year}_weather.csv', index=False)

def combine():
    # adapted code from https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
    files = [TEMP_DIR+'/'+file for file in os.listdir(TEMP_DIR)]
    dfs = list()
    for i, f in enumerate(files):
        data = pd.read_csv(f)
        dfs.append(data)
    df = pd.concat(dfs, ignore_index=True)

    df.sort_values('date', inplace=True)
    weatherdir = '../data/curated/weather/'
    if not os.path.exists(weatherdir):
        os.makedirs(weatherdir)

    df.to_csv(f'{weatherdir}/laguardia.csv', index=False)

    print(df.describe())

def test():
    print(os.getcwd())
if __name__ == '__main__':
    #clean(range(2017, 2020))
    #combine()
    test()
