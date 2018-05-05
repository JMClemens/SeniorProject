import re
import csv
import pygeoip
from collections import Counter
from collections import OrderedDict
from collections import namedtuple
from collections import defaultdict
import datetime
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
kDurationFile = "kdur.csv"
kDurationTableFile = "kdurbottom.csv"
loginRatioFile = "kloginratio.csv"
top10LoginFile = "kTop10Login.csv"


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
		
		times = re.findall(r'[0-60]{2}\:[0-9][0-9]\:[0-9][0-9]\:*', session)
		if not times:
			pass
		else:
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
			if len(times) == 1:
				startTime = times.pop(0)
				duration = 1
			elif len(times) > 1:
				startTime = times.pop(0)
				endTime = times.pop(len(times)-1)
				duration = get_sec(str(endTime)) - get_sec(str(startTime))
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

def parseTodaysLog():
	global sessionList
	log = logPath + "kippo.log." + str(datetime.date.today())
	parseLog(log)
	fullActivityList = []
	with open('kp/csv/kippo_all.csv', 'r') as file:
		reader = csv.DictReader(file)
		for row in reader:
				fullActivityList.append(row)
	combList = fullActivityList + [x for x in sessionList if x not in fullActivityList]
	sessionList = combList
	
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
			else:
				oneTo2000.append(item['Country'])
		else:
			top10.append(item)
		counter = counter + 1
	outsideTop = OrderedDict([("Over 1000",oneTo2000),("501-1000",fiveTo1000),("301-500",threeTo500),("101-300",oneTo300),("51-100",fiftyTo100),("1-50",oneTo50)])
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

def make_bins(x_in, n_bins):  
    """
    x_in is a list of numbers
    n_bins is how many bins to separate x into
    returns a list of length of n_bins, each element of which is a list
    """
    x_min = min(x_in)
    x_max = max(x_in)
    x = [[] for _ in range(n_bins)]
    for a in x_in:
        # compute the bin number for value a
        n = int(float(a - x_min) / (x_max - x_min + 1.0) * n_bins)
        x[n].append(a)
    return x  # x is a binned list of elements from x_in
	
	
def getDurationInfo():
	durationList = []
	# List to hold our different categories
	# 6-12 minutes, ... in intervals of 6 mins
	first = 0
	second = 0
	third = 0
	fourth = 0
	fifth = 0
	sixth = 0
	seventh = 0
	eigth = 0
	ninth = 0
	tenth = 0
	
	for item in sessionList:
		durationList.append(int(item["Duration"]))
	
	
	# Get all items over 6 minutes
	hitCounter = Counter(durationList)
	hitCounter = dict(hitCounter)
	for key,value in hitCounter.items():
		if key <= 360:
			pass
		elif key <= 720:
			second = second + value
		elif key <= 1080:
			third = third + value
		elif key <= 1440:
			fourth = fourth + value
		elif key <= 1800:
			fifth = fifth + value
		elif key <= 2160:
			sixth = sixth + value
		elif key <= 2520:
			seventh = seventh + value
		elif key <= 2880:
			eigth = eigth + value
		elif key <= 3240:
			ninth = ninth + value
		else:
			tenth = tenth + value
	freqDict = OrderedDict([("6m-12m",second),("12m-18m",third),("18m-24m",fourth),("24m-30m",fifth),("30m-36m",sixth),("36m-42m",seventh),("42m-48m",eigth),("48m-54m",ninth),("54-60m+",tenth)])

	# Get all items under 6 minutes, 1 minutes through 6 minutes
	sortedTimeByMin = sorted([0 if x < 0 else x / 60 for x in durationList])
	timeCounts = Counter(sortedTimeByMin)
	timeCounts = dict(timeCounts)
	counter = 0
	oneThrough6mins = []
	totalThrough6 = 0
	for key,value in timeCounts.items():
		if key == counter and counter <= 6:
			oneThrough6mins.append({"Session Duration (mins)":key, "Number of Sessions":value})
			totalThrough6 += value
		else:
			pass
		counter += 1			
	oneThrough6mins.append({"Session Duration (mins)":"Total", "Number of Sessions":totalThrough6})
	# Write to 2 separate CSV files
	# One for the graph and one for the table
	write_list_of_dicts_to_csv(kDurationTableFile, oneThrough6mins)
	write_dict_to_csv(kDurationFile, ["Duration","Sessions"],freqDict)


def getLoginAttempts():
		loginList = []
		for item in sessionList:
			loginList.append(item["LoginAttempts"])
		
		fixedList = []
		for item in loginList:
			if len(item) > 0:
				for login in item:
					fixedList.append(login)
		
		userPassList = []
		numSucceded = 0
		numFailed = 0
		for item in fixedList:
			mo = re.search(r'\[(.*)\]', item)
			data = mo.group(1)
			userPassList.append(data)
			
			if "succeeded" in item:
				numSucceded = numSucceded + 1
			elif "failed" in item:
				numFailed = numFailed + 1
			else:
				"Unknown input - pass"
				pass

		loginFreq = Counter(userPassList) 
		loginFreq = dict(loginFreq)
		sortedLogins = OrderedDict(sorted(loginFreq.items(), key=lambda t: t[1], reverse=True))
		
		top10UserPass = []
		counter = 0
		
		for key, value in sortedLogins.items():
			if counter < 10:
				entry = {"Login":key,"Frequency":value}
				top10UserPass.append(entry)
			else:
				pass
			counter = counter + 1
		
		failedSuccess = OrderedDict([("Succeeded",numSucceded),("Failed",numFailed)])
		write_dict_to_csv(loginRatioFile, ["Login Status","Number of Logins"], failedSuccess)
		write_list_of_dicts_to_csv(top10LoginFile, top10UserPass)
	
def selectAction(x):
		if x == "-all":
			parseAllLogs()
		#	dailyActivityTotals()
		#	countryFrequency()
		#	getDurationInfo()
			getLoginAttempts()
			print "Kippo Logs Parsed"
		elif x == "-today":
			parseTodaysLog()
			dailyActivityTotals()
			countryFrequency()
			getDurationInfo()
			print "Current Kippo Log Parsed"
		else:
			pass

if __name__ == '__main__':
	selectAction(*sys.argv[1:])