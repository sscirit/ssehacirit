## Script for GFS Ensemble Runs both primary and secondary files

import boto3
from os import makedirs

def download_gribs(date, model_hour, ensemble_num, start_hour, n_hours, grib_save_path, hour_diff=3):
    s3cli = boto3.client("s3")
    bucket = "noaa-gefs-pds"
    model_hour = str(model_hour).zfill(2)
    ensemble_num = str(ensemble_num).zfill(2)
    template = f"gefs.{date}/{model_hour}/atmos/pgrb2ap5/gep{ensemble_num}.t{model_hour}z.pgrb2a.0p50.fHOUR"
    keys = [template.replace("HOUR", str(start_hour+ i*hour_diff).zfill(3)) for i in range(n_hours//hour_diff)]
    for key in keys:
        filename=key.split("/")[-1]
        save_path = f"{grib_save_path}/{date}_A/{ensemble_num}/{filename}"
        save_path_b = save_path.replace("_A", "_B")
        makedirs("/".join(save_path.split("/")[:-1]), exist_ok=True)
        makedirs("/".join(save_path_b.split("/")[:-1]), exist_ok=True)
        s3cli.download_file(Bucket=bucket, Key=key, Filename=save_path)
        s3cli.download_file(Bucket=bucket, Key=key.replace("pgrb2a", "pgrb2b"), Filename=save_path_b)
