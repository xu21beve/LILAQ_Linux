import requests
import json
from datetime import date, timedelta
import sys
import csv
import os

config = "/home/aerosol/Documents/Quant-AQ/config.json"
start_day = date.today() - timedelta(days=1)
end_day = date.today() - timedelta(days=1) # start date = end date to get 1 day's worth of data
#config = "../../config/summer-2024.json"

with open(config) as fp:
    settings = json.load(fp)

api_base = settings['sources']['quant-aq']['api']
quant_api_key = settings['sources']['quant-aq']['api-key']

# Support both "start_timestamp" and "start-timestamp"
# start_day = date.fromisoformat(
#     settings.get("start_timestamp") or settings.get("start-timestamp")
# )
# end_day = date.fromisoformat(
#     settings.get("end_timestamp") or settings.get("end-timestamp")
# )

def try_get(url):
    response = requests.get(url, auth=(quant_api_key, ''))
    if response.status_code == 200:
        return response.json().get('data')
    else:
        print('error!', response.status_code, file=sys.stderr)
        return []

def day_range(start_day, end_day):
    this_day = start_day
    while this_day <= end_day:
        yield this_day
        this_day += timedelta(days=1)

def flatten_dict(d, prefix=""):
    new_d = {}
    for key, val in d.items():
        if prefix: label = f'{prefix}_{key}'
        else: label = key
        if type(val) == dict:
            inner = flatten_dict(val, prefix = label)
            for inner_key, inner_val in inner.items():
                new_d[inner_key] = inner_val
        else:
            new_d[label] = val
    return new_d

def get_sensor_data(quant, type=''):
    day_url = f'{api_base}/devices/{quant}/data-by-date/'
    if type: day_url += f'{type}/'

    headers = None
    for this_day in day_range(start_day, end_day):
        response = try_get(f'{day_url}/{this_day}')
        print(f"Fetching data for {this_day} (device {quant}, type={type})")
        for result in map(flatten_dict, response):
            if headers is None:
                headers = list(result.keys())
                if type:
                    yield [f'{type}_{h}' for h in headers]
                else:
                    yield [f'final_{h}' for h in headers]
            yield [result[h] for h in headers]

def get_all_data():
    data_dir = os.path.join(settings["data-dir"], settings["sources"]["quant-aq"]["path"])
    os.makedirs(data_dir, exist_ok = True)
    for device in try_get(f'{api_base}/devices'):
        device_id = device['sn']

        data_gen = get_sensor_data(device_id)
        """
        Raw returns data every minute, not corrected for temp/humidity
        Final returns data every minute, corrected for temp/humidity
        """
        raw_data_gen = get_sensor_data(device_id, "raw")
        data_gen = get_sensor_data(device_id)

        combfname = os.path.join(data_dir, f'{device_id}-combined.csv')
        indfname = os.path.join(data_dir, f'{device_id}.csv')

        # Removing Firebase writing for now, since it's an API call and can be accessed online
        # Write to daily files (for Firebase efficient upload)
        # with open(indfname, 'w', newline='') as csvfile:
        #     writer = csv.writer(csvfile)
        #     for row, raw_row in zip(data_gen, raw_data_gen):
        #         writer.writerow(row + raw_row)

        # Write to aggregated files (for Google Drive long-term storage)
        with open(combfname, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row, raw_row in zip(data_gen, raw_data_gen):
                writer.writerow(row + raw_row)

get_all_data()
