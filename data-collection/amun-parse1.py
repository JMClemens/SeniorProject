import pygeoip
import getCenterCords as g
import csv
from collections import Counter
from collections import OrderedDict
from collections import defaultdict
from itertools import groupby
import os
import re
import datetime
import time
import sys

logPath = "am/logs/"
csvPath = "am/csv/"
aCountryFrequencyFile = "acf.csv"
aTop10CountriesFile = "aTop10C.csv"
aOtherCountriesFile = "aOtherC.csv"
aDailyHitsFile = "adailyhits.csv"
aPortCounts = "apc.csv"
aPortFrequency = "aports.csv"
allLog = "amun_all.csv"
shellActivity = "ashell.csv"
requestActivity = "arequest.csv"
vulnActivity = "avuln.csv"
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

def write_dict_to_csv(fileName, fieldnames, myDict):
	os.chdir('am/csv')
	with open(fileName, 'wb') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow([k for k in fieldnames])
		for key, value in myDict.items():
			 writer.writerow([key, value])
	os.chdir('../../')
			
def getAllLogs():
	os.chdir('am/logs')
	logs = os.listdir('.')
	os.chdir('../../')
	return logs

def parseLog(fileName):
	with open(fileName, "r") as file:
		if "shellcode" in fileName:
			for line in file:
				contents = line.split()
				date = contents[0]
				secondGroup = contents[1].split(",")
				timeStamp = secondGroup[0]
				statusCode = secondGroup[1]
				ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', line)
				if ip:
					ipAddr = ip.pop(0)
					ipAddr = ''.join(c for c in ipAddr if c not in '()')
					countryName = gip.country_name_by_addr(ipAddr)
				else:
					ipAddr = 'none'
					countryName = "Unknown"
				
				if "EternalBlue" in line:
					activity = "EternalBlue SMB Vulnerability"
				elif "IIS Vulnerability" in line:
					activity = "Microsoft IIS Vulnerability"
				elif "Unknown" in line:
					activity = "Unknown"
				elif "PortScan" in line:
					activity = "PortScan"
				else:
					activity = "unclassified"
				
				entry = {'Date':date, "Timestamp":timeStamp, "StatusCode":statusCode, "IP":ipAddr, "Country":countryName, "Port":"443","Activity":activity}
				shellCodeActivity.append(entry)
		elif "request" in fileName:
			pattern = '(?P<port>[0-9]*).*'
			for line in file:
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
				if countryName == '':
					countryName = "Unknown"
				
				checkStages= re.search(r'Stages: \[(.*)\]', line)
				if checkStages:
					str = checkStages.group(0)
					activity = re.findall(r'\[(.*)\]', str)[0]
					activity = activity.replace("\'", "")
					activity = activity.strip("\"")
				elif "PortScan" in line:
					activity = "PortScan"
				else:
					activity = "unclassified"
				
				
				entry = {"Port":port,"IP":ipAddr,"Date":dateStamp,"Timestamp":timeStamp,"Status Code":statusCode,"Country":countryName,"Activity":activity}
				requestHandlerActivity.append(entry)
		elif "vulnerabilities" in fileName:
			# commands for parsing vulnerabilities logs
			pass
		else:
			print "Unable to process log " + fileName
			pass
		
					
def parseAllLogs():
	logs = getAllLogs()
	for file in logs:
		myFile = logPath + file
		parseLog(myFile)
	allList = shellCodeActivity + requestHandlerActivity +vulnLogInfo
	write_list_of_dicts_to_csv(allLog, allList)
	write_list_of_dicts_to_csv(shellActivity, shellCodeActivity)
	write_list_of_dicts_to_csv(requestActivity, requestHandlerActivity)
	write_list_of_dicts_to_csv(vulnActivity, vulnLogInfo)

def parseTodaysLog():
	global shellCodeActivity
	global requestHandlerActivity
	global vulnLogInfo
	shellLog = logPath + "shellcode_manager.log." + str(datetime.date.today())
	requestLog = logPath + "amun_request_handler.log." + str(datetime.date.today())
	vulnLog = logPath + "vulnerabilities.log." + str(datetime.date.today())
	logs = [shellLog, requestLog, vulnLog]
	for log in logs:
		parseLog(log)
	
	fullShellActivity = []
	fullRequestActivity = []
	fullVulnActivity = []
	with open(csvPath+shellActivity,'r') as file:
		reader = csv.DictReader(file)
		for row in reader:
				fullShellActivity.append(row)
	with open(csvPath+requestActivity,'r') as file:
		reader = csv.DictReader(file)
		for row in reader:
				fullRequestActivity.append(row)
	with open(csvPath+vulnActivity,'r') as file:
		reader = csv.DictReader(file)
		for row in reader:
				fullVulnActivity.append(row)
	combShell = fullShellActivity + [x for x in shellCodeActivity if x not in fullShellActivity]
	shellCodeActivity = combShell
	combReq = fullRequestActivity + [x for x in requestHandlerActivity if x not in fullRequestActivity]
	requestHandlerActivity = combReq
	combVuln = fullShellActivity + [x for x in vulnLogInfo if x not in fullVulnActivity]
	vulnLogInfo = combVuln
	
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
		
	countryGraphAndTableFiles(newCountryList)
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

def countryGraphAndTableFiles(countryList):
	sortedCountryList = sorted(countryList,key=lambda x:x['Frequency'], reverse=True)
	top10 = []
	oneTo10 = []
	tenTo30 = []
	thirty1To50 = []
	fiftyTo100 = []
	over100 = []
	
	counter = 0
	for item in sortedCountryList:
		if counter > 9:
			if item['Frequency'] <= 10:
				oneTo10.append(item['Country'])
			elif item['Frequency'] <= 30:
				tenTo30.append(item['Country'])
			elif item['Frequency'] <= 50:
				thirty1To50.append(item['Country'])
			elif item['Frequency'] <= 100:
				fiftyTo100.append(item['Country'])
			else:
				over100.append(item['Country'])
		else:
			top10.append(item)
		counter = counter + 1
	outsideTop = OrderedDict([("Over 100",over100),("51-100",fiftyTo100),("31-50",thirty1To50),("11-30",tenTo30),("1-10",oneTo10)])
	write_list_of_dicts_to_csv(aTop10CountriesFile,top10)
	write_dict_to_csv(aOtherCountriesFile, ["Number of Hits","Countries"],outsideTop)	
				
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

def canonicalize_dict(x):
    "Return a (key, value) list sorted by the hash of the key"
    return sorted(x.items(), key=lambda x: hash(x[0]))

def unique_and_count(lst):
    "Return a list of unique dicts with a 'count' key added"
    grouper = groupby(sorted(map(canonicalize_dict, lst)))
    return [dict(k + [("count", len(list(g)))]) for k, g in grouper]	
	
def portActivities():
	activityList = []
	for item in shellCodeActivity:
		activityList.append({"Port":item["Port"],"Activity":item["Activity"]})
	for item in requestHandlerActivity:
		activityList.append({"Port":item["Port"],"Activity":item["Activity"]})
	activities = unique_and_count(activityList)
	for item in activities:
		print item
	
	act = defaultdict(list)
	for d in activities:
		for key, value in d.iteritems():
			act[key].append(value)
			
	
def selectAction(x):
		if x == "-all":
			parseAllLogs()
			countryFrequency()
			dailyActivityTotals()
			portTotals()
			portActivities()
			print "Amun Logs Parsed"
		elif x == "-today":
			parseTodaysLog()
			countryFrequency()
			dailyActivityTotals()
			portTotals()
			print "Current Amun Log Parsed"
		else:
			pass

if __name__ == '__main__':
	selectAction(*sys.argv[1:])

