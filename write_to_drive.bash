#!/bin/bash

# Use metData as a temp log file (using read_wxt.py)
# Parse temp log file data at the end of the day
python3 text_to_csv.py

# Add today's data in metData.csv to a long-running file called metDataFull.csv
metDataCSV="/home/HawkinsPi/metData.csv"
metDataFullCSV="/home/HawkinsPi/metDataFull.csv"
if [ ! -s "$metDataFullCSV" ]; then
    cat "$metDataCSV" >> "$metDataFullCSV"
else
    # Remove the first row if there is already data in metDataFull.csv
    sed '1d' "$metDataCSV" >> "$metDataFullCSV"
fi

# Upload the long-running CSV to the Drive
rclone copy $metDataFullCSV LILAQ:MetSensor
rclone copy /home/HawkinsPi/quant-aq/ LILAQ:QuantAQ # Upload yesterday's QuantAQ data