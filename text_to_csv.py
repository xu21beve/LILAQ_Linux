from datetime import date, datetime, timedelta
from glob import glob
import json
import sys
import csv
import os
import re

config = "/home/HawkinsPi/config.json"
#config = "../../config/summer-2024.json"

with open(config) as fp:
    settings = json.load(fp)

data_dir = settings["data-dir"]
# met_dir = os.path.join(data_dir, settings["sources"]["met"]["path"])
met_glob = settings["sources"]["met"]["glob"]
# start_day = date.fromisoformat(settings['start_timestamp'])
# end_day = date.fromisoformat(settings['end_timestamp'])

def get_all_data(f_path, output_dir):
    split_re = re.compile("(?:,|\s*\~\s*)")
    def parse_line(line):
        if not(line.strip()): return None, {}
        parts = [x for x in split_re.split(line.strip()) if x]
        command = parts[2]
        if command != '0r0': return None, {}
        timestamp=datetime.fromisoformat(",".join(parts[:1]))
        message = parts[3:-1] # skip id at the end
        d = dict([x.split('=') for x in message if x])
        return timestamp, d

    # f_path = os.path.join(met_dir, met_glob)
    yesterday_string = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
    # f_path = f"/home/HawkinsPi/metData.{yesterday_string}"
    out_name = os.path.join(output_dir, "metData.csv")
    header = None
    file_list = glob(f_path)
    with open(file_list[0]) as fp:
        for line in fp.readlines():
            _, d = parse_line(line)
            if d: header = sorted(d.keys())
    with open(out_name, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Timestamp"] + header)
        for fname in file_list:
            with open(fname) as inp:
                for line in inp.readlines():
                    timestamp, d = parse_line(line)
                    if d:
                        row = [timestamp] + [d.get(h,'')[:-1]for h in header]
                        writer.writerow(row)

yesterday_string = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
get_all_data(f"/home/HawkinsPi/metData.{yesterday_string}","/home/HawkinsPi/") # Convert full log files to CSVs
get_all_data("/home/HawkinsPi/data-buffer/metData","/home/HawkinsPi/data-buffer/") # Convert metData buffer file to CSV
# get_all_data("/home/HawkinsPi/data-buffer/quant-aq") # Convert QuantAQ buffer file to CSV (this should be running on the desktop in the lab)