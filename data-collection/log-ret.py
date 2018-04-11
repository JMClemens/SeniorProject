'''
Log retrieval script for gathering logs from:
Glastopf Honeypot
Amun Honeypot

Run using:
sudo python log-ret.py [-option]
Values for [-option]
-g : Collect all glastopf logs
-a : Collect all amun logs

Authored by Joshua Clemens for CS475 at Hood College
'''
import datetime
import os
import subprocess
import sys

glastopfLogPath = '../jmc/glastopf/financialfirstgroup/log/'
glastopfLogDestinationPath = "../jmc/gl/logs"
glastopfLogs = []

amunLogPath = '../jmc/amun/logs/'
amunLogDestinationPath = "../jmc/am/logs/"
acceptedLogs = ['shellcode','request','vulnerabilities']

kippoLogPath = '../caw/kippo/kippo/log/'
kippoLogDestinationPath = "../jmc/kp/logs/"

def getAllGlastopfLogs():

	# Get all files in the glastopf log directory 
	logs = [f for f in os.listdir(glastopfLogPath) if os.path.isfile(os.path.join(glastopfLogPath, f))]
	
	# Copy each file over
	for log in logs:
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
	keptLogs = []
	
	for log in logs:
		if any(x in log for x in acceptedLogs):
			keptLogs.append(log)
		else:
			pass
	
	for log in keptLogs:
		subprocess.Popen(["scp", amunLogPath+log, amunLogDestinationPath]).wait()

		
def getAllKippoLogs():
	
	# Get all files in the Kippo log directory
	logs = [f for f in os.listdir(kippoLogPath) if os.path.isfile(os.path.join(kippoLogPath, f))]
	
	# Copy files to local directory for backup & dating
	for log in logs:
		subprocess.Popen(["scp", kippoLogPath+log, kippoLogDestinationPath]).wait()
	

	
	# Date logs
	for log in logs:
		dateList = []
		with open(kippoLogDestinationPath+log, "r") as file:
			for line in file:
				contents = line.split()
				date = contents[0]
				if date not in dateList:
					dateList.append(date)
				else:
		print "Info from log: "
		print log
		print dateList
				
def writeLineToFile(fileName, line):
	
		
def selectLogs(x):
	if x == "-g":
		getAllGlastopfLogs()
		print "Glastopf logs retrieved"
	elif x == "-a":
		getAllAmunLogs()
		print "Amun logs retrieved"
	elif x == "-k":
		getAllKippoLogs()
		print "Kippo logs retrieved"
	else:
		pass

# Main function - Calls the selectLogs function with the command line argument
# Use -g to collect all glastopf logs
# Use -a to collect all amun logs
if __name__ == '__main__':
	selectLogs(*sys.argv[1:])