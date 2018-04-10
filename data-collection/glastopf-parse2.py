import pygeoip
import getCenterCords as g
import csv
from collections import Counter
from collections import OrderedDict
import os
import re
import datetime

fileName = "glastopf.log"
outFile = "glastopf.csv"
allLog = "all.csv"
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
ignoreLine = ["Initializing Glastopf","Connecting to main database", "Glastopf started", "Bootstrapping dork database","Generating initial dork pages","Stopping Glastopf","File successfully parsed with sandbox","Failed to fetch injected file","Traceback (most recent call last)","File \"","URLError","injected_file","3210#\"! "]

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

def write_dict_to_csv(fileName,fieldNames, myDict):
	os.chdir('gl/csv')
	with open(fileName,"wb") as out_file:
		fieldnames = fieldNames
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writer.writerow
		for key, value in myDict.items():
			writer.writerow([key, value])

def getAllLogs():
	os.chdir('gl/logs')
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
		lines = file.readlines()
		last = lines[-1]
		for line in lines:
			# ignore lines that don't add any graphical values
			if any(x in line for x in ignoreLine):
				pass
			elif line is last:
				print "Pass"
				pass
			else:	
				contents = line.split()
				date = contents[0]
				secondGroup = contents[1].split(",")
				print "Line"
				print line
				print "Second group"
				print secondGroup
				timeStamp = secondGroup[0]
				httpStatusCode = secondGroup[1]
				ipAddr = contents[3]
				httpRequestMethod = contents[5]
				requestedResource = contents[6]
				countryName =  gip.country_name_by_addr(ipAddr)
				if requestedResource == "/": requestedResource = "index.html"

				entry = {"Date":date, "Timestamp":timeStamp, "IP":ipAddr, "Country":countryName, "StatusCode":httpStatusCode,"RequestMethod":httpRequestMethod,"Resource":requestedResource}
				print entry
				activityList.append(entry)
					
def parseAllLogs():
	logs = getAllLogs()
	for file in logs:
		myFile = logPath + file
		parseLog(myFile)
	write_list_of_dicts_to_csv(allLog, activityList)



def is_ascii(s):
	return all(ord(c) < 128 for c in s)
	
def countryFrequency():
	countryList = []
	for item in activityList:
		countryList.append(item["Country"])
	countryFrequency = Counter(countryList)
	countryFrequency = dict(countryFrequency)
	newCountryList = []
	for key, value in countryFrequency.items():
		coords = g.get_boundingbox_country(country=key, output_as='center')
		entry = {"Country":key,"Frequency":value,"Coords":coords}
		newCountryList.append(entry)
	write_list_of_dicts_to_csv(gCfreqFile,newCountryList)	

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
	timeFrequency = Counter(timeList)
	timeFrequency = dict(timeFrequency)
	newTimeList = []
	for key, value in timeFrequency.items():
		entry = {"Timestamp":key,"Count":value}
		newTimeList.append(entry)
	sortedTimeList = sorted(newTimeList,key=lambda x:x['Timestamp'])
	write_list_of_dicts_to_csv(gTimeOfDayFile,sortedTimeList)
	
# TODO:
# make this function only include GET requests
# make similar functions for other types of requests

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
	print topURI
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





#parseLog(fileName)
#write_list_of_dicts_to_csv(outFile,activityList)
parseAllLogs()
#countryFrequency()
#requestFrequency()
#resourceFrequency()
#dailyActivityTotals()
#statusCodeFrequency()
timeOfDay()