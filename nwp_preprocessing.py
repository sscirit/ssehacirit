def nwp_preprocess_ensemble(nwp_type, file_path):
    """
    NWP Preprocess Section
        Suitable for Long Format Any NWP Dataset that contain:
                forecast_epoch, lat, lon, variable, value, level
    """
    nwp_data = pd.read_csv(file_path, compression='gzip')
    nwp_data["Date"] = pd.to_datetime(nwp_data.forecast_epoch, unit='s')
    nwp_data.sort_values(by="Date", ascending=True)
    nwp_data.set_index("Date",inplace=True)

    lat_lon = np.unique(nwp_data.lat.astype(str) + '_' + nwp_data.lon.astype(str))
    levels = nwp_data.level.unique()

    nwp_data["infos"] = nwp_data["Ensemble"].astype(str) + "_" + nwp_data["lat"].astype(str) + "_" + nwp_data["lon"].astype(str) + "_" + nwp_data["variable"] + "_" + nwp_data["level"]
    nwp_data = nwp_data.pivot_table(values=['value'], index=['Date'], columns=['infos'])

    nwp_ws_results = {}
    for coords in lat_lon:
        for level in levels:
            for ens_num in range(21):
                nwp_ws_results[f"{nwp_type}{str(ens_num).zfill(2)}_{coords}_{level}"] = np.sqrt(nwp_data["value",f"{ens_num}_{coords}_UGRD_{level}"]**2 + nwp_data["value",f"{ens_num}_{coords}_VGRD_{level}"]**2)

    nwp_ws_results = pd.DataFrame(nwp_ws_results)
    
    return nwp_ws_results

wrf = nwp_preprocess_ensemble("WRF", "/home/user/Desktop/ensemble_wrf_data.csv")
