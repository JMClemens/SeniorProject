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
logPath = "gl/logs/"
csvPath = "gl/csv/"
gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)
ignoreLine = ["Initializing Glastopf","Connecting to main database", "Glastopf started", "Bootstrapping dork database","Generating initial dork pages","Stopping Glastopf","3210#"]

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
	print logs
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
		for line in file:
			print line
			if any(x in line for x in ignoreLine):
				pass
			else:	
				contents = line.split()
				date = contents[0]
				secondGroup = contents[1].split(",")
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
				#print entry
				activityList.append(entry)

def parseAllLogs():
	logs = getAllLogs()
	for file in logs:
		myFile = logPath + file
		parseLog(myFile)
	write_list_of_dicts_to_csv(allLog, activityList)


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
		entry = {"Request":key,"Frequency":value}
		newRequestList.append(entry)
	write_list_of_dicts_to_csv(gRfreqFile,newRequestList)	

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
	write_list_of_dicts_to_csv(gResourceFile,newResourceList)	

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
write_list_of_dicts_to_csv(outFile,activityList)
parseAllLogs()
#countryFrequency()
requestFrequency()
resourceFrequency()
dailyActivityTotals()