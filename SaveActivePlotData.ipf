#pragma rtGlobals=3		// Use modern global access method and strict wave access.
// See general Igor Pro documentation here: https://docs.wavemetrics.com/igorpro/commands/make
	
Function SaveActivePlotData(filename)
	String filename // Name for output specified on function call
	
	// Since we know which entries we want, let's actually set waveList to a constant:
	String waveList = "root:Time_Series:NH4, root:Time_Series:Org, root:Time_Series:SO4, root:Time_Series:NO3, root:Time_Series:Chl"
	
	// Set data folder 
	String folderPath = "root:Time_Series:"
	
	// Set saved data target path. /O overwrites an existing file with the same name
	NewPath/O/C exportPath, "C:ACSM:ACSMData:ScanData:SavedGraphData:"
	
	// Save current folder location so that we can return during cleanup
	String currentDF = GetDataFolder(1)
	
	// Assign time wave to local variable
	String timeWaveStr = "root:ACSM_Incoming:acsm_local_time"
	WAVE timeWave = $timeWaveStr
	
	// Path to reformatted text time wave (we'll use this new wave to parameterize our data)
	String timeTextPath = "root:ACSM_Incoming:time_text"

	// Allocate memory for an empty time wave. /O overwrites existing waveList
	// with name conflict, /T makes a text wave, /N=n makes a wave with n points
	Make/O/T/N=(numpnts(timeWave)) $timeTextPath

	// Assign our empty time wave to a WAVE variable
	WAVE/T twt = $timeTextPath
	
	// Perform the secs2date and Secs2Time operations on all points p in the timeWave
	// Secs2Date: format = -2 (YYYY-MM-DD)
	// Secs2Time: format = 3 (military time with seconds)
	twt = Secs2Date(timeWave[p], -2) + " " + Secs2Time(timeWave[p], 3)
	
	// Append our reformated time wave to the list of waves we want to export
	String commaList = timeTextPath + ", " + waveList
	
	// Move to folder with time series
	SetDataFolder $folderPath
	
	// Using Save instead of SaveData in order to export data as a CSV
	// /J saves as deliminted text, /W includes wave names as header row
	String cmd
	sprintf cmd, "Save /O /J /W /P=exportPath %s as \"%s\"", commaList,  filename

	// Executing the cmd we created a string to prevent accidental character escapes
	Execute cmd
	
	// Return to original folder for clean closure
	SetDataFolder $currentDF
	
	Print "Saved data from active plot to: " + filename
End