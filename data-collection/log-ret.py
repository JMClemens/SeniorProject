'''
Log retrieval script for gathering logs from:
Glastopf Honeypot
Amun Honeypot
Kippo Honeypot

Run using:
sudo python log-ret.py [-option]
Values for [-option]
-g : Collect all glastopf logs
-a : Collect all amun logs
-k : Collect all kippo logs
-gc: Collect current glastopf log
-ac: Collect current amun logs
-kc: Collect current kippo log

Authored by Joshua Clemens for CS475 at Hood College
'''
import datetime
import os
import subprocess
import sys
import re

glastopfLogPath = '../jmc/glastopf/financialfirstgroup/log/'
glastopfLogDestinationPath = "../jmc/gl/logs"
glastopfLogs = []

amunLogPath = '../jmc/amun/logs/'
amunLogDestinationPath = "../jmc/am/logs/"
acceptedLogs = ['shellcode','request','vulnerabilities']

kippoLogPath = '../caw/kippo/kippo/log/'
kippoLogDestinationPath = "../jmc/kp/logs/"

def getAllGlastopfLogs():

	print "Getting Glastopf Logs"
	# Get all files in the glastopf log directory 
	logs = [f for f in os.listdir(glastopfLogPath) if os.path.isfile(os.path.join(glastopfLogPath, f))]
	
	# Copy each file over
	for log in logs:
		subprocess.Popen(["scp", glastopfLogPath+log, glastopfLogDestinationPath]).wait()
	
	
	# Rename current day's log to be timestamped
	os.chdir(glastopfLogDestinationPath)
	subprocess.Popen(["scp", "glastopf.log", "glastopf.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","glastopf.log"]).wait()
	os.chdir("../../")
	

def getCurrentGlastopfLog():
	
	print "Getting current Glastopf log"
	# Get today's log
	log = glastopfLogPath + "glastopf.log"
	subprocess.Popen(["scp", log, glastopfLogDestinationPath]).wait()
	
	# Rename current day's log to be timestamped
	os.chdir(glastopfLogDestinationPath)
	subprocess.Popen(["scp", "glastopf.log", "glastopf.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","glastopf.log"]).wait()
	os.chdir("../../")
	
def getAllAmunLogs():
	
	print "Getting Amun logs"
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

	# Rename current day's logs to be timestamped
	os.chdir(amunLogDestinationPath)
	subprocess.Popen(["scp", "amun_request_handler.log", "amun_request_handler.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","amun_request_handler.log"]).wait()
	subprocess.Popen(["scp", "shellcode_manager.log", "shellcode_manager.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","shellcode_manager.log"]).wait()
	subprocess.Popen(["scp", "vulnerabilities.log", "vulnerabilities.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","vulnerabilities.log"]).wait()
	os.chdir("../../")
	
def getCurrentAmunLogs():

	print "Getting current Amun logs"
	
	# Get all of the logs we're interested in
	aLog = amunLogPath + "amun_request_handler.log"
	sLog = amunLogPath + "shellcode_manager.log"
	vLog = amunLogPath + "vulnerabilities.log"
	
	logs = [aLog,sLog,vLog]
	
	for log in logs:
		subprocess.Popen(["scp", log, amunLogDestinationPath]).wait()
		
	# Rename current day's logs to be timestamped
	os.chdir(amunLogDestinationPath)
	subprocess.Popen(["scp", "amun_request_handler.log", "amun_request_handler.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","amun_request_handler.log"]).wait()
	subprocess.Popen(["scp", "shellcode_manager.log", "shellcode_manager.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","shellcode_manager.log"]).wait()
	subprocess.Popen(["scp", "vulnerabilities.log", "vulnerabilities.log."+str(datetime.date.today())]).wait()
	subprocess.Popen(["rm","vulnerabilities.log"]).wait()
	os.chdir("../../")
	
		
def getAllKippoLogs():
	print "Getting Kippo Logs"
	# Get names of all files in the Kippo log directory
	logs = [f for f in os.listdir(kippoLogPath) if os.path.isfile(os.path.join(kippoLogPath, f))]
	
	# Copy files to local directory for backup & dating
	for log in logs:
		subprocess.Popen(["scp", kippoLogPath+log, kippoLogDestinationPath]).wait()
		
	print "Dating Kippo Logs"
	# Get log dates and write to new files based on their dates
	for log in logs:
		datePattern = re.compile(r'\d{4}-\d{2}-\d{2}')
		with open(kippoLogDestinationPath+log, "r") as file:
			for line in file:
				if datePattern.match(line):
					match = re.search(r'\d{4}-\d{2}-\d{2}',line)
					date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').strftime("%Y-%m-%d")
					outFile = "kp/logs/dated/kippo.log." + date
					with open(outFile, "a+") as file:
						file.write(line)

		
def getCurrentKippoLog():
	print "Getting current Kippo log"
	# Get the path to the current kippo logs
	log = kippoLogPath + "kippo.log"
	# Get log dates and write to new file(s) based on their dates
	datePattern = re.compile(r'\d{4}-\d{2}-\d{2}')
	with open(log, "r") as file:
		for line in file:
			if datePattern.match(line):
					match = re.search(r'\d{4}-\d{2}-\d{2}',line)
					date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').strftime("%Y-%m-%d")
					outFile = "kp/logs/kippo.log." + date
					with open(outFile, "a+") as file:
						file.write(line)
						
def selectLogs(x):
	if x == "-g":
		getAllGlastopfLogs()
		print "Glastopf Logs Retrieved"
	elif x == "-gc":
		getCurrentGlastopfLog()
		print "Current Glastopf Log Retrieved"
	elif x == "-a":
		getAllAmunLogs()
		print "Amun Logs Retrieved"
	elif x == "-ac":
		getCurrentAmunLogs()
		print "Current Amun logs Retrieved"
	elif x == "-k":
		getAllKippoLogs()
		print "Kippo Logs Retrieved"
	elif x == "-kc":
		getCurrentKippoLog()
		print "Current Kippo Log Retrieved"
	else:
		pass

# Main function - Calls the selectLogs function with the command line argument
# Use -g to collect all glastopf logs
# Use -a to collect all amun logs
# Use -k to collect all kippo logs
# Use -gc to collect current glastopf log
# Use -ac to collect current amun logs
# Use -kc to collect current kippo log

if __name__ == '__main__':
	selectLogs(*sys.argv[1:])