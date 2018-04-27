import pygeoip
import getCenterCords as g
import csv
from collections import Counter
from collections import OrderedDict
import os
import re
import datetime
import time
import sys

logPath = "am/logs/"
csvPath = "am/csv/"
aCountryFrequencyFile = "acf.csv"
aDailyHitsFile = "adailyhits.csv"
aPortCounts = "apc.csv"
aPortFrequency = "aports.csv"
allLog = "amun_all.csv"
gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)

shellCodeActivity = []
requestHandlerActivity = []
vulnLogInfo = []

def write_list_of_dicts_to_csv(fileName, list_of_dicts):
	os.chdir('am/csv')
	with open(fileName,"wb") as out_file:
		fieldnames = sorted(list(set(k for d in list_of_dicts for k in d)))
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writeheader()
		for row in list_of_dicts:
		    writer.writerow(row)
		os.chdir('../../')

def write_parsed_info_to_csvs():
	os.chdir('am/csv')
	infoList = shellCodeActivity + requestHandlerActivity
	write_list_of_dicts_to_csv("amun_all.csv",infoList)
			
def getAllLogs():
	os.chdir('am/logs')
	logs = os.listdir('.')
	os.chdir('../../')
	return logs

def parseLog(fileName):
	with open(fileName, "r") as file:
		if "shellcode" in fileName:
			print "Shellcode manager parsing..."
			for line in file:
				print type(line)
				contents = line.split()
				print contents
				date = contents[0]
				secondGroup = contents[1].split(",")
				timeStamp = secondGroup[0]
				statusCode = secondGroup[1]
				ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
				ipAddr = ip[0]
				#ipAddr = ''.join(c for c in ipAddr if c not in '()')
				countryName = gip.country_name_by_addr(ipAddr)
				entry = {'Date':date, "Timestamp":timeStamp, "StatusCode":statusCode, "IP":ipAddr, "Country":countryName, "Port":"443"}
				shellCodeActivity.append(entry)
		elif "request" in fileName:
			print "Request handler parsing..."
			pattern = '(?P<port>[0-9]*).*'
			for line in file:
				print line
				match = re.search(r"Port:\s[0-9]+", line)
				if match:
						result = match.group(0)
						port = ''.join(c for c in result if c.isdigit())
				else:
						port = ""
				ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', line)
				if ip:
					ipAddr = ip.pop(0)
					ipAddr = ''.join(c for c in ipAddr if c not in '()')
				else:
					ipAddr = 'none'
					
				contents = line.split()
				dateStamp = contents[0]
				secondGroup = contents[1].split(",")
				timeStamp = secondGroup[0]
				statusCode = secondGroup[1]
				countryName = gip.country_name_by_addr(ipAddr)
				entry = {"Port":port,"IP":ipAddr,"Date":dateStamp,"Timestamp":timeStamp,"Status Code":statusCode,"Country":countryName}
				print entry
				requestHandlerActivity.append(entry)
		elif "vulnerabilities" in fileName:
			# commands for parsing vulnerabilities logs
			print "Vulnerabilities log parsing..."
		else:
			print "Unable to process log " + fileName
			pass
		
					
def parseAllLogs():
	logs = getAllLogs()
	for file in logs:
		myFile = logPath + file
		parseLog(myFile)
	allList = shellCodeActivity + requestHandlerActivity
	write_list_of_dicts_to_csv(allLog, allList)
	
def countryFrequency():
	
	# Build our list of countries to check
	shellCountryList = []
	requestCountryList = []
	for item in shellCodeActivity:
		shellCountryList.append(item["Country"])
	for item in requestHandlerActivity:
		requestCountryList.append(item["Country"])
	
	# check frequencies of our countries in all logs
	#	and turns to dict with combined info
	requestCountryFrequency = Counter(requestCountryList)
	countryFrequency = Counter(shellCountryList)
	countryFrequency = dict(countryFrequency+requestCountryFrequency)
	
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
	write_list_of_dicts_to_csv(aCountryFrequencyFile,newCountryList)	

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
	
def timeOfDay():
	timeList = []
	for item in shellCodeActivity:
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

def dailyActivityTotals():
	shellDailyTotal = []
	handlerDailyTotal = []
	for item in shellCodeActivity:
		shellDailyTotal.append(item["Date"])
	for item in requestHandlerActivity:
		handlerDailyTotal.append(item["Date"])
	handlerHits = sorted(handlerDailyTotal, key=lambda d: map(int, d.split('-')))
	hits = sorted(shellDailyTotal, key=lambda d: map(int, d.split('-')))
	handlerHitCounter = Counter(handlerHits)
	hitCounter = Counter(hits)
	hitCounter = dict(hitCounter+handlerHitCounter)
	newHitCounter = OrderedDict(sorted(hitCounter.items(), key=lambda t: t[0]))
	newHitList = []
	for key, value in newHitCounter.items():
		entry = {"DateStamp":key,"NumHits":value}
		newHitList.append(entry)
	write_list_of_dicts_to_csv(aDailyHitsFile,newHitList)	
	
def portTotals():
	spTotals = []
	rpTotals = []
	for item in shellCodeActivity:
		spTotals.append(item["Port"])
	for item in requestHandlerActivity:
		rpTotals.append(item["Port"])
	spCounter = Counter(spTotals)
	rpCounter = Counter(rpTotals)
	portCounter = dict(spCounter + rpCounter)
	newPortList = []
	for key, value in portCounter.items():
		entry = {"Port":key,"Count":value}
		newPortList.append(entry)
	write_list_of_dicts_to_csv(aPortCounts,newPortList)	

def selectAction(x):
		if x == "-all":
			parseAllLogs()
			countryFrequency()
			dailyActivityTotals()
			portTotals()
			print "Amun Logs Parsed"
		elif x == "-today":
			parseTodaysLog()
			countryFrequency()
			dailyActivityTotals()
			portTotals()
			print "Current Glastopf Log Parsed"
		else:
			pass

if __name__ == '__main__':
	selectAction(*sys.argv[1:])

