## This script wrote for ECMWF Open Access 0.4 Degree Weather Data
## It downloads latest gribs of every run hour for Day t-1

import os
import pandas as pd
from datetime import datetime

url_main = "https://data.ecmwf.int/forecasts/"

sys_date = datetime.strftime(datetime.now(), format = "%Y%m%d")
grib_date = datetime.strftime(datetime.now() - pd.to_timedelta(1, "d"), format = "%Y%m%d")
print("")
print(f"This ECMWF Data is downloading on {sys_date} & downloaded for {grib_date}")

def ecmwf_gribber(date: str, hr: int, run: int):
    """
    date = "%Y%m%d"
    hr = "0,6,12,18"
    run = "3,6" 
    """
    run, hr = str(run), str(hr).zfill(2)

    tof = ["scda" if (hr == "06") | (hr == "18") else "oper"][0]
    
    url_secondary = f"{date}/{hr}z/0p4-beta/{tof}/{date}{hr}0000-{run}h-{tof}-fc.grib2"
    url_temp = url_main + url_secondary
    
    if not os.path.exists(f"/home/user/Desktop/ECMWFGribs/{date}/{hr}/"):
        os.makedirs(f"/home/user/Desktop/ECMWFGribs/{date}/{hr}/")
        print("...The File Created...")
    else:
        print("...The File already exists!!...")
        
    os.chdir(f"/home/user/Desktop/ECMWFGribs/{date}/{hr}/")
    os.system(f"wget {url_temp}")


for hr in range(0,19,6):
    for run in range(3,7,3):
        ecmwf_gribber(grib_date, hr, run)
