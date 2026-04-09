# Igor Procedure, Python scripts, and Windows Batch scripts for ACSM realtime data upload

## Data Flow (Flow repeats every day in 15 minute intervals)
1. **Data Query**: After Igor Pro fetches and analyzes data from the ACSM, `SaveActivePlotData.ipf` is run using a Windows Batch file (need to get this from Github)
    - `SaveActivePlotData.ipf` is in the `Igor Procedures` folder
    - `SaveActivePlotData.ipf` must be saved in the current Igor instance. (In Igor, go to `File`>`Open file`>`Procedures`>`SaveActivePlotData.ipf`).
2. **Data Backup**: To save a copy of the most recent data from the ACSM for diff checking, `backup_data.bat` runs.
3. **Diff Checker**: To catalog which new rows have been added to the data set, `diff_checker.py` runs.
4. **Data Uploader**: To upload the new rows to Firestore Database, `firebase/write_to_firebase.py` runs.

### Notes
- `write_to_firebase.py` writes upload logs to `upload_log.txt`
- `diff_checker.py` and `write_to_firebase.py` write error logs to `error_log.txt`
- All scripts are run using Windows Task Scheduler with the following settings: 
    - Repeats every 15 minutes
    - Recurs daily
    - Runs for the duration of a day
- For the ACSM, the plot data we are uploading is always called `Time_series_plot`.
- To customize this script for other sensors running Igor (e.g. the SEMS), you'll need to: 
    - Change target wave names in `SaveActivePlotData.ipf`
    - Change local filepaths in `SaveActivePlotData.ipf`, `backup_data.bat`, and `firebase/write_to_firbase.py`, and `diff_checker.py`
    - Change the target Firestore Database collection in `firebase/write_to_firebase.py`
