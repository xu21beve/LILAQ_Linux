#pragma rtGlobals=3		// Use modern global access method and strict wave access.
	
Function SaveActivePlotData(filename)
	String filename // Name for output specified on function call
	
	// Since we know which entries we want, let's actually set waveList to a constant:
	String waveList = "root:Time_Series:NH4, root:Time_Series:Org, root:Time_Series:SO4, root:Time_Series:NO3, root:Time_Series:Chl"
	
	// Find data folder
	// WAVE w = TraceNameToWaveRef("", StringFromList(0, waveList))
	String folderPath = "root:Time_Series:"
	
	// Set target path. /O overwrites an existing file with the same name
	NewPath/O/C exportPath, "C:ACSM:ACSMData:ScanData:SavedGraphData:"
	
	// Save graph data to target folder
	String currentDF = GetDataFolder(1) // Save current data folder location
	
	// Create temporary time wave with datetime format
	String timeWaveStr = "root:ACSM_Incoming:acsm_local_time"
	WAVE timeWave = $timeWaveStr
	
	// Create text time wave to reformat
	String timeTextPath = "root:ACSM_Incoming:time_text"

	Make/O/T/N=(numpnts(timeWave)) $timeTextPath
	WAVE/T twt = $timeTextPath
	
	twt = secs2date(timeWave[p], -2) + " " + Secs2Time(timeWave[p], 3)
	
	String commaList = timeTextPath + ", " + waveList
	
	SetDataFolder $folderPath
	Print folderPath
	Print GetDataFolder(1)
	
	// Using Save instead of SaveData in order to export data as a CSV
	// /J saves as deliminted text, /W includes wave names as header row
	// Save /B /J /W /O /P=exportPath waveList as filename
	String cmd
	sprintf cmd, "Save /O /J /W /P=exportPath %s as \"%s\"", commaList,  filename
	Execute cmd
	// Save /O /J /W /P=exportPath $commaList as filename
	
	// Return to original folder for clean closure
	SetDataFolder $currentDF
	
	Print "Saved data from active plot to: " + filename
End