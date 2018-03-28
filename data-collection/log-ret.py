import datetime
import os
import subprocess

glastopfLogPath = '../jmc/glastopf/financialfirstgroup/log/'
glastopfLogDestinationPath = "glogs"
glastopfLogs = []

def getAllGlastopfLogs():

	# Get all files in the glastopf log directory 
	logs = [f for f in os.listdir(glastopfLogPath) if os.path.isfile(os.path.join(glastopfLogPath, f))]
	
	# Copy each file over
	for log in logs:
		subprocess.Popen(["scp", glastopfLogPath+log, glastopfLogDestinationPath]).wait()

	# Rename current day's log to be timestamped
	os.chdir(glastopfLogDestinationPath)
	subprocess.Popen(["scp", glastopfLogPath+"glastopf.log ", glastopfLogDestinationPath+"glastopf.log."+str(datetime.date.today())]).wait()

getAllGlastopfLogs()