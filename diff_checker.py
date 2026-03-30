from datetime import datetime
import os

# Creates a file which is the diff between file 1 and file 2
def diff_checker(path1, path2, output_path):
	with open(path1, 'r') as f1:
		# Using set avoid duplicates and is faster than a list
		f1_lines = {line for line in f1}
	
	with open(path2, 'r') as f2, open(output_path, 'a') as out:
		added_header = False
		for line in f2:
			# Add first row of column headers if buffer.txt is empty
			if os.path.getsize(output_path) == 0 and not added_header:
				print(line, file=out, end="")
				added_header = True
			if line not in f1_lines:
				print(line, file=out, end="")

# Old data is backed up into local data upload folder by Windows Batch script backup_data.bat
local_dir = "C:\\Users\\acsm.ACSMC-087\\Documents\\GitHub\\"
ACSM_dir = "C:\\ACSM\\ACSMData\\ScanData\\SavedGraphData\\"
data_fname = "Time_Series_" + datetime.now().strftime("%Y%m%d") + ".txt"

old_data = local_dir + "data\\" + data_fname 
new_data = ACSM_dir + data_fname
output_path = local_dir + "data\\buffer.txt"
log_file = local_dir + "error_log.txt"

# Attempt to create diff file
try:
	diff_checker(old_data, new_data, output_path)
except Exception as e:
	with open(local_dir + 'error_log.txt', 'a') as out:
		print(datetime.now().strftime("%Y%m%d%T") + str(e), file=out)