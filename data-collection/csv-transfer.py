'''
Data transfer script to move data from local user space
to visualization dashboard

Run using:
sudo python csv-transfer.py [-option]
Values for [-option]
-g : Copy Glastopf data to dashboard
-a : copy Amun data to dashboard
-k : Copy Kippo data to dashboard
-all: Copy all data to dashboard

Authored by Joshua Clemens for CS475 at Hood College
'''
import datetime
import os
import subprocess
import sys
import re

glastopfCSVPath = '../jmc/gl/csv/'
amunCSVPath = '../jmc/am/csv/'
kippoCSVPath = "../jmc/kp/csv/"
destinationPath = '../../../../var/www/financialfirstgroup.com/public_html/assets/data/'


def copyData(mypath):

	# Get our CSV files and store them into a list
	csvs = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
	
	# Copy each file to the web dashboard data diretory
	for file in csvs:
		subprocess.Popen(["scp", mypath+file, destinationPath]).wait()

def copyGlastopfData():
	copyData(glastopfCSVPath)
	
def copyAmunData():
	copyData(amunCSVPath)

def copyKippoData():
	copyData(kippoCSVPath)	
	
def copyAllFiles():
	copyGlastopfData()
	copyAmunData()
	copyKippoData()
						
def selectFiles(x):
	if x == "-g":
		copyGlastopfData()
		print "Glastopf Data Sent to Dashboard"
	elif x == "-a":
		copyAmunData()
		print "Amun Data Sent to Dashboard"
	elif x == "-k":
		copyKippoData()
		print "Kippo Data Sent to Dashboard"
	elif x == "-all":
		copyAllFiles()
		print "All Data Sent to Dashboard"
	else:
		print "Command not regonized." + "\nUse -g to copy all Glastopf CSV data files to dashboard website"
		+ "\nUse -a to copy all Amun CSV data files to dashboard website" 
		+ "\nUse -k to copy all Kippo CSV data files to dashboard website"
		+ "\nUse -all to copy all CSV data files to dashboard website"

# Main function - Calls the selectLogs function with the command line argument
# Use -g to copy all Glastopf CSV data files to dashboard website
# Use -a to copy all Amun CSV data files to dashboard website
# Use -k to copy all Kippo CSV data files to dashboard website
# Use -all to copy all CSV data files to dashboard website

if __name__ == '__main__':
	selectFiles(*sys.argv[1:])