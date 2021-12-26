def process_nwp_wind(nwp_name: str, nwp: pd.DataFrame, isEnsemble: bool):
    
    nwp_raw = nwp
    nwp_raw["variable"] = nwp_raw["variable"].str.cat(nwp_raw["level"], sep="_")
    if isEnsemble == False:
        nwp_raw["variable"] = nwp_name + "_" + nwp_raw["variable"]
    elif isEnsemble == True:
        nwp_raw["variable"] = nwp_name + "_" + nwp_raw["ens_num"].astype(str) + "_" + nwp_raw["variable"] 
    levels = nwp_raw['level'].unique()
    nwp_raw = nwp_raw.drop(columns="level")
    lat_lon = nwp_raw["lat"].astype(str).str.cat(nwp_raw["lon"].astype(str), sep="_")
    lat_lon.drop_duplicates(inplace=True)
    lat_lon = lat_lon.to_list()

    nwp_raw = nwp_raw.pivot_table(
        index="forecast_epoch",
        columns=["variable", "lat", "lon"],
        values="value",
    )
    nwp_raw.columns = nwp_raw.columns.map("{0[0]}_{0[1]}_{0[2]}".format)

    nwp_raw_results = pd.DataFrame()
    
    if isEnsemble == True:
        for coords in lat_lon:
            for level in levels:
                for ens_num in range(31):
                    try:
                        nwp_raw_results[f"{nwp_name}{str(ens_num).zfill(2)}_WS_{level}_{coords}"] = np.sqrt(nwp_raw[f'{nwp_name}_{ens_num}_UGRD_{level}_{coords}']**2 + nwp_raw[f'{nwp_name}_{ens_num}_VGRD_{level}_{coords}']**2)
                        nwp_raw_results[f"{nwp_name}{str(ens_num).zfill(2)}_wdir_{level}_{coords}"] = (180 + 180*np.arctan2(nwp_raw[f'{nwp_name}_{ens_num}_VGRD_{level}_{coords}'],nwp_raw[f'{nwp_name}_{ens_num}_UGRD_{level}_{coords}']))%360
                    except KeyError:
                        pd.DataFrame()
    elif isEnsemble == False:
        for coords in lat_lon:
            for level in levels:
                try:
                    nwp_raw_results[f"{nwp_name}_WS_{level}_{coords}"] = np.sqrt(nwp_raw[f'{nwp_name}_UGRD_{level}_{coords}']**2 + nwp_raw[f'{nwp_name}_VGRD_{level}_{coords}']**2)
                    nwp_raw_results[f"{nwp_name}_wdir_{level}_{coords}"] = (180 + 180*np.arctan2(nwp_raw[f'{nwp_name}_VGRD_{level}_{coords}'],nwp_raw[f'{nwp_name}_UGRD_{level}_{coords}']))%360
                except KeyError:
                    pd.DataFrame()
    
    nwp_raw_results.reset_index(inplace=True)
    nwp_raw_results["Date"] = pd.to_datetime(nwp_raw_results.forecast_epoch,unit='s')
    nwp_raw_results.set_index("Date",inplace=True)
    nwp_raw_results.drop(columns=['forecast_epoch'],inplace=True)
            
    return nwp_raw_results
