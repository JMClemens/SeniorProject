import pygeoip
import getCenterCords as g
import csv
from collections import Counter
from collections import OrderedDict
import os
import re
import datetime
import time

logPath = "am/logs/"
csvPath = "am/csv/"
aCountryFrequencyFile = "acf.csv"
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

def write_dict_to_csv(fileName,fieldNames, myDict):
	os.chdir('am/csv')
	with open(fileName,"wb") as out_file:
		fieldnames = fieldNames
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writer.writerow
		for key, value in myDict.items():
			writer.writerow([key, value])

def getAllLogs():
	os.chdir('am/logs')
	logs = os.listdir('.')
	os.chdir('../../')
	return logs

def getLogDate(fileName):
	if fileName != 'glastopf.log':
		match = re.findall(r'\d{4}-\d{2}-\d{2}', fileName)
		if match:
			mymatch = match[0]
			date = datetime.datetime.strptime(mymatch, '%Y-%m-%d').date()
		else:
			date = datetime.date.today()
	else:
		date = datetime.date.today()
		date = datetime.datetime(*(date.timetuple()[:3]))
		date = date.strftime('%Y-%m-%d')

	return date

def parseLog(fileName):
	with open(fileName, "r") as file:
		if "shellcode" in fileName:
			print "Shellcode manager parsing..."
			for line in file:
				contents = line.split()
				date = contents[0]
				secondGroup = contents[1].split(",")
				timeStamp = secondGroup[0]
				statusCode = secondGroup[1]
				ipAddr = contents[4]
				ipAddr = ''.join(c for c in ipAddr if c not in '()')
				countryName = gip.country_name_by_addr(ipAddr)
				entry = {'Date':date, "Timestamp":timeStamp, "StatusCode":statusCode, "IP":ipAddr, "Country":countryName}
				shellCodeActivity.append(entry)
		elif "request" in fileName:
			# commands for parsing request handler logs
			print "Request handler parsing..."
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
	write_list_of_dicts_to_csv(allLog, activityList)
	
def countryFrequency(myList):
	countryList = []
	for item in myList:
		countryList.append(item["Country"])
	countryFrequency = Counter(countryList)
	countryFrequency = dict(countryFrequency)
	newCountryList = []
	for key, value in countryFrequency.items():
		coords = g.get_boundingbox_country(country=key, output_as='center')
		entry = {"Country":key,"Frequency":value,"Coords":coords}
		newCountryList.append(entry)
	write_list_of_dicts_to_csv(aCountryFrequencyFile,newCountryList)	
	
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

parseLog(logPath+"shellcode_manager.log")



