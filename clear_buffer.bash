#!/bin/bash

# Clear buffer after it has been uploaded
head -n 1 "/home/HawkinsPi/data-buffer/metData.csv" > tmpfile && mv tmpfile "/home/HawkinsPi/data-buffer/metData.csv"
echo "" > "/home/HawkinsPi/data-buffer/metData"

echo "Data buffers cleared." >> log.txt