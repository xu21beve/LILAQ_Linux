@echo off
FOR /F "delims=" %%a IN ('powershell -Command "[DateTime]::Today.ToString('yyyyMMdd')"') DO SET TODAY_DATE=%%a
COPY /Y "C:\ACSM\ACSMData\ScanData\SavedGraphData\Time_Series_%TODAY_DATE%.txt" C:\Users\acsm.ACSMC-087\Documents\GitHub\data\Time_Series_%TODAY_DATE%.txt