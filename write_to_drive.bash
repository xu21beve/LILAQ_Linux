#!/bin/bash

# Yesterday's Quant AQ data
quant_aq_data_dir="/home/aerosol/Documents/Quant-AQ/data/quant-aq/"

# Upload the long-running CSV to the Drive
rclone copy $quant_aq_data_dir LILAQ:QuantAQ
