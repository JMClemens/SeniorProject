import datetime
import os
import subprocess

glastopfLogPath = '../jmc/glastopf/financialfirstgroup/log/'
glastopfLogDestinationPath = "../jmc/gl/logs"
glastopfLogs = []

amunLogPath = '../jmc/amun/logs/'
amunLogDestinationPath = "../jmc/am/logs/"

def getAllGlastopfLogs():

	# Get all files in the glastopf log directory 
	logs = [f for f in os.listdir(glastopfLogPath) if os.path.isfile(os.path.join(glastopfLogPath, f))]
	
	# Copy each file over
	for log in logs:
		print "CWD:"
		print os.getcwd();
		print "Log:"
		print log
		print "Path: " + glastopfLogPath + log
		print "Dest Path: " + glastopfLogDestinationPath
		subprocess.Popen(["scp", glastopfLogPath+log, glastopfLogDestinationPath]).wait()
	
	'''
	# Rename current day's log to be timestamped
	os.chdir(glastopfLogDestinationPath)
	subprocess.Popen(["sudo scp", "glastopf.log", "glastopf.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","glastopf.log"]).wait()
	os.chdir("../../")
	'''

def getAllAmunLogs():
	
	# Get all files in the amun log directory
	logs = [f for f in os.listdir(amunLogPath) if os.path.isfile(os.path.join(amunLogPath, f))]
	
	for log in logs:
		print log
	
	# Copy each file over
	for log in logs:
		print "CWD:"
		print os.getcwd();
		print "Log:"
		print log
		print "Path: " + amunLogPath + log
		print "Dest Path: " + amunLogDestinationPath
		subprocess.Popen(["scp", amunLogPath+log, amunLogDestinationPath]).wait()
	
getAllGlastopfLogs()