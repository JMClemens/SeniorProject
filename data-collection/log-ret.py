import datetime
import os
import subprocess

glastopfLogPath = '../jmc/glastopf/financialfirstgroup/log/'
glastopfLogs = []

def getAllGlastopfLogs():
	logs = [f for f in os.listdir(glastopfLogPath) if os.path.isfile(os.path.join(glastopfLogPath, f))]
	for log in logs:
		subprocess.Popen(["scp", log, "glogs"]).wait()

getAllGlastopfLogs()