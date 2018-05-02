import re
import csv
import pygeoip
from collections import Counter
from collections import OrderedDict
from collections import namedtuple
import os
import sys

gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)
logPath = "kp/logs/dated/"
csvPath = "kp/csv/"
kCountryFreqFile = "kcf.csv"
allActivity = "kippo_all.csv"
kTop10CountriesFile = "kTop10C.csv"
kOtherCountriesFile = "kOtherC.csv"
kDailyHitsFile = "kdailyhits.csv"

sessionList = []

# Helper function for string timestamp to int seconds
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def getAllLogs():
	os.chdir(logPath)
	logs = os.listdir('.')
	os.chdir('../../../')
	return logs

def write_list_of_dicts_to_csv(fileName, list_of_dicts):
	os.chdir(csvPath)
	with open(fileName,"wb") as out_file:
		fieldnames = sorted(list(set(k for d in list_of_dicts for k in d)))
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writeheader()
		for row in list_of_dicts:
		    writer.writerow(row)
		os.chdir('../../')

def write_dict_to_csv(fileName, fieldnames, myDict):
	os.chdir('kp/csv')
	with open(fileName, 'wb') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow([k for k in fieldnames])
		for key, value in myDict.items():
			 writer.writerow([key, value])
	os.chdir('../../')
	
def parseLog(logFile):
	log = open(logFile, "r").read()

	conn_list = re.split("(New connection:.*)",log)

	for session in conn_list:
		ip =  re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', session)
		if ip:
			ip = ip.pop(0)
		else:
			ip = 'none'
	
		# Extract the date from our session
		dates = re.findall(r'\d{4}-\d{2}-\d{2}',logFile)
		date = dates.pop(0)
		
		la = re.findall("login attempt.*", session)
		times = re.findall(r'[0-60]{2}\:[0-9][0-9]\:[0-9][0-9]\:*', session)
		if len(times) > 1:
			startTime = times.pop(0)
			endTime = times.pop(len(times)-1)
			duration = get_sec(str(endTime)) - get_sec(str(startTime))
			m, s = divmod(duration, 60)
			h, m = divmod(m, 60)
			duration = "%02d:%02d:%02d" % (h, m, s)
		else:	
			startTime = 0
			endTime = 0
			duration = 0

		if ip != 'none':
			countryName = gip.country_name_by_addr(ip)
			if countryName =="Hong Kong": countryName = "China"
		else:
			countryName = 'Unknown'
			
		entry = {"IP":ip, "Duration":duration, "LoginAttempts":la, "Country":countryName, "Timestamp":startTime, "Date":date}
		sessionList.append(entry)
		
def parseAllLogs():
	logs = getAllLogs()
	for file in logs:
		myfile = logPath + file
		parseLog(myfile)
	write_list_of_dicts_to_csv(allActivity, sessionList)

def countryFrequency():

	# Build our list of countries to check
	countryList = []
	for item in sessionList:
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
	
	countryGraphAndTableFiles(newCountryList)
	write_list_of_dicts_to_csv(kCountryFreqFile,newCountryList)	
	
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
	oneTo50 = []
	fiftyTo100 = []
	oneTo300 = []
	threeTo500 = []
	fiveTo1000 = []
	oneTo2000 = []
	over2000 = []
	
	counter = 0
	for item in sortedCountryList:
		if counter > 9:
			if item['Frequency'] <= 50:
				oneTo50.append(item['Country'])
			elif item['Frequency'] <= 100:
				fiftyTo100.append(item['Country'])
			elif item['Frequency'] <= 300:
				oneTo300.append(item['Country'])
			elif item['Frequency'] <= 500:
				threeTo500.append(item['Country'])
			elif item['Frequency'] <= 1000:
				fiveTo1000.append(item['Country'])
			elif item['Frequency'] <= 2000:
				oneTo2000.append(item['Country'])
			else:
				over2000.append(item['Country'])
		else:
			top10.append(item)
		counter = counter + 1
	fields = ["1-5","5-15","> 15"]
	outsideTop = OrderedDict([("Over 2000",over2000),("1000-2000",oneTo2000),("500-1000",fiveTo1000),("300-500",threeTo500),("100-300",oneTo300),("50-100",fiftyTo100),("1-50",oneTo50)])
	write_list_of_dicts_to_csv(kTop10CountriesFile,top10)
	write_dict_to_csv(kOtherCountriesFile, ["Number of Hits","Countries"],outsideTop)				

def dailyActivityTotals():
	dailyHitsTotal = []
	for item in sessionList:
		dailyHitsTotal.append(item["Date"])
	hits = sorted(dailyHitsTotal, key=lambda d: map(int, d.split('-')))
	hitCounter = Counter(hits)
	hitCounter = dict(hitCounter)
	newHitCounter = OrderedDict(sorted(hitCounter.items(), key=lambda t: t[0]))
	newHitList = []
	for key, value in newHitCounter.items():
		entry = {"DateStamp":key,"NumHits":value}
		newHitList.append(entry)
	write_list_of_dicts_to_csv(kDailyHitsFile,newHitList)	
	
def selectAction(x):
		if x == "-all":
			parseAllLogs()
			dailyActivityTotals()
			countryFrequency()
			print "Kippo Logs Parsed"
		elif x == "-today":
			parseTodaysLog()
			print "Current Kippo Log Parsed"
		else:
			pass

if __name__ == '__main__':
	selectAction(*sys.argv[1:])