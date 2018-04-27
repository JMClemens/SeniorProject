import pygeoip
import getCenterCords as g
import csv
from collections import Counter
from collections import OrderedDict
from collections import namedtuple
import os
import re
import datetime
import time
import sys

fileName = "glastopf.log"
outFile = "glastopf.csv"
allLog = "glastopf_all.csv"
gCfreqFile = "gcf.csv"
gRfreqFile = "grf.csv"
gResourceFile = "gresrcf.csv"
gDailyHitsFile =  "gdailyhits.csv"
gTopURIFile = "gURI.csv"
gStatusCodesFile = "gStatus.csv"
gTimeOfDayFile = "gTimeOfDay.csv"
logPath = "gl/logs/"
csvPath = "gl/csv/"
gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)
ignoreLine = ["Initializing Glastopf","Connecting to main database", "Glastopf started", "Bootstrapping dork database","Generating initial dork pages","Stopping Glastopf","File successfully parsed with sandbox","Failed to fetch injected file","Traceback (most recent call last)"]

activityList = []

def write_list_of_dicts_to_csv(fileName, list_of_dicts):
	os.chdir('gl/csv')
	with open(fileName,"wb") as out_file:
		fieldnames = sorted(list(set(k for d in list_of_dicts for k in d)))
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writeheader()
		for row in list_of_dicts:
		    writer.writerow(row)
		os.chdir('../../')

def getAllLogs():
	os.chdir('gl/logs')
	logs = os.listdir('.')
	os.chdir('../../')
	return logs

def parseLog(fileName):
	with open(fileName, "r") as file:
		lines = file.readlines()
		last = lines[-1]
		for line in lines:
			# ignore lines that don't add any graphical values
			if any(x in line for x in ignoreLine):
				pass
			elif line is last:
				pass
			else:	
				contents = line.split()
				date = contents[0]
				secondGroup = contents[1].split(",")
				timeStamp = secondGroup[0]
				httpStatusCode = secondGroup[1]
				ipAddr = contents[3]
				httpRequestMethod = contents[5]
				requestedResource = contents[6]
				countryName =  gip.country_name_by_addr(ipAddr)
				if countryName == '':
					countryName = "Unknown"
				if requestedResource == "/": requestedResource = "index.html"
				entry = {"Date":date, "Timestamp":timeStamp, "IP":ipAddr, "Country":countryName, "StatusCode":httpStatusCode,"RequestMethod":httpRequestMethod,"Resource":requestedResource}
				activityList.append(entry)
					
def parseAllLogs():
	logs = getAllLogs()
	for file in logs:
		myFile = logPath + file
		parseLog(myFile)
	write_list_of_dicts_to_csv(allLog, activityList)
	
def parseTodaysLog():
	global activityList
	log = logPath + "glastopf.log." + str(datetime.date.today())
	parseLog(log)
	fullActivityList = []
	with open('gl/csv/all.csv', 'r') as file:
		reader = csv.DictReader(file)
		for row in reader:
				fullActivityList.append(row)
	combList = fullActivityList + [x for x in activityList if x not in fullActivityList]
	activityList = combList
	
def countryFrequency():

	# Build our list of countries to check
	countryList = []
	for item in activityList:
		countryList.append(item["Country"])
	countryFrequency = Counter(countryList)
	countryFrequency = dict(countryFrequency)
	
	# Load coordinate list
	coordList = []
	with open('google-coordinates.csv', 'r') as file:
		reader = csv.DictReader(file)
		for row in reader:
			coordList.append(row)
	
	# Build CSV file with coordinate and frequency info
	newCountryList = []
	for key, value in countryFrequency.items():
		coords = getCountryCoordinates(key, coordList)
		entry = {"Country":key,"Frequency":value,"Coords":coords}
		newCountryList.append(entry)
	write_list_of_dicts_to_csv(gCfreqFile,newCountryList)	
	
def getCountryCoordinates(country,coordList):
	if country == "Europe":
		coords = [float(60),float(60)]
		return coords
	elif country == "Unknown":
		coords = [float(30),float(-40)]
		return coords
	else:
		for item in coordList:
			if item["name"] == country:
				coords = [float(item["latitude"]),float(item["longitude"])]
				return coords

def requestFrequency():
	requestList = []
	for item in activityList:
		requestList.append(item["RequestMethod"])
	requestFrequency = Counter(requestList)
	requestFrequency = dict(requestFrequency)
	newRequestList = []
	for key, value in requestFrequency.items():
		entry = {"Frequency":value,"Request":key,}
		newRequestList.append(entry)
	write_list_of_dicts_to_csv(gRfreqFile,newRequestList)	

def statusCodeFrequency():
	codeList = []
	for item in activityList:
		codeList.append(item["StatusCode"])
	codeFrequency = Counter(codeList)
	codeFrequency = dict(codeFrequency)
	newCodeList = []
	for key, value in codeFrequency.items():
		entry = {"StatusCode":key,"Count":value}
		newCodeList.append(entry)
	write_list_of_dicts_to_csv(gStatusCodesFile,newCodeList)
	
def timeOfDay():
	timeList = []
	for item in activityList:
		timeList.append(item["Timestamp"])
	removeSecs = []
	for item in timeList:	
		tempTimes = item.split(':')
		newTime = tempTimes[0] + ":" + tempTimes[1]
		removeSecs.append(newTime)
	timeFrequency = Counter(removeSecs)
	timeFrequency = dict(timeFrequency)
	newTimeList = []
	for key, value in timeFrequency.items():
		entry = {"Timestamp":key,"Count":value}
		newTimeList.append(entry)
	sortedTimeList = sorted(newTimeList,key=lambda x:x['Timestamp'])
	write_list_of_dicts_to_csv(gTimeOfDayFile,sortedTimeList)

def resourceFrequency():
	resourceList = []
	for item in activityList:
		resourceList.append(item["Resource"])
	resourceFrequency = Counter(resourceList)
	resourceFrequency = dict(resourceFrequency)
	newResourceList = []
	for key, value in resourceFrequency.items():
		entry = {"Resource":key,"Frequency":value}
		newResourceList.append(entry)
	sortedResourceList = sorted(newResourceList,key=lambda x:x['Frequency'], reverse=True)
	topURI = []
	counter = 0
	for item in sortedResourceList:
		if counter > 9:
			break
		elif 'index.html' in item.values() or '/favicon.ico' in item.values() or '/style.css' in item.values():
			pass
		else:
			topURI.append(item)
			counter = counter + 1
	write_list_of_dicts_to_csv(gTopURIFile, topURI)
	write_list_of_dicts_to_csv(gResourceFile,sortedResourceList)	

def dailyActivityTotals():
	dailyHitsTotal = []
	for item in activityList:
		dailyHitsTotal.append(item["Date"])
	hits = sorted(dailyHitsTotal, key=lambda d: map(int, d.split('-')))
	hitCounter = Counter(hits)
	hitCounter = dict(hitCounter)
	newHitCounter = OrderedDict(sorted(hitCounter.items(), key=lambda t: t[0]))
	newHitList = []
	for key, value in newHitCounter.items():
		entry = {"DateStamp":key,"NumHits":value}
		newHitList.append(entry)
	write_list_of_dicts_to_csv(gDailyHitsFile,newHitList)	

def selectAction(x):
		if x == "-all":
			parseAllLogs()
			write_list_of_dicts_to_csv(outFile,activityList)
			countryFrequency()
			requestFrequency()
			resourceFrequency()
			dailyActivityTotals()
			statusCodeFrequency()
			timeOfDay()
			print "Glastopf Logs Parsed"
		elif x == "-today":
			parseTodaysLog()
			write_list_of_dicts_to_csv(outFile,activityList)
			countryFrequency()
			requestFrequency()
			resourceFrequency()
			dailyActivityTotals()
			statusCodeFrequency()
			timeOfDay()
			print "Current Glastopf Log Parsed"
		else:
			pass

if __name__ == '__main__':
	selectAction(*sys.argv[1:])