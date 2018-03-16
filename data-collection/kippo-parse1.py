import re
import csv
import pygeoip
import getCenterCords as g
from collections import Counter
import os

gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)
sessionList = []
logkCfreqFile = "klog.csv"
dkCfreqFile = "kdur.csv"
outFile = "kippo.csv"
kCfreqFile = "kcf.csv"
logFile = "kippo.log"
logPath = "kippo/logs/"
csvPath = "kippo/csv/"

# Helper function for string timestamp to int seconds
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# Writes our log info to a csv file
def write_list_of_dicts_to_csv(fileName, list_of_dicts):
	os.chdir('kippo/csv')
	with open(fileName,"wb") as out_file:
		fieldnames = sorted(list(set(k for d in list_of_dicts for k in d)))
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writeheader()
		for row in list_of_dicts:
		    writer.writerow(row)
		os.chdir('../../')


def parseLog(logFile):
	log = open(logFile, "r").read()

	conn_list = re.split("(New connection:.*)",log)

	for session in conn_list:
		
		#print "-------- Session Start ---------"
		ip =  re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', session)
		if ip:
			ip = ip.pop(0)
		else:
			ip = 'none'
		
		la = re.findall("login attempt.*", session)
		#for line in la:
		#	print "IP addr: " + ip  + "  \nLogin Attempts: " + line
		
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
			if countryName == "Korea, Republic of": countryName = "South Korea"
			elif countryName =="Hong Kong": countryName = "China"
		#	print(countryName)
		else:
			country = 'none'

		if countryName != 'none':
			#coords = g.get_boundingbox_country(country=countryName, output_as='center')
			coords = 'none'
		else:
			coords = 'none'

		# Readd coords once that part is fixed
		entry = {"IP":ip, "Duration":duration, "Log":la, "Country":countryName}
		sessionList.append(entry)

		#print "-------- Session End ---------"

def countryFrequency():
	countryList = []
	for item in sessionList:
		countryList.append(item["Country"])
	countryFrequency = Counter(countryList)
	countryFrequency = dict(countryFrequency)
	newCountryList = []
	for key, value in countryFrequency.items():
		#coords = g.get_boundingbox_country(country=key, output_as='center')
		#add coords when solution is found
		entry = {"Country":key,"Frequency":value}
		newCountryList.append(entry)
	write_list_of_dicts_to_csv(kCfreqFile,newCountryList)

def durationFrequency():
	durationList = []
	for item in sessionList:
		durationList.append(item["Duration"])
	durationFrequency = Counter(durationList)
	durationFrequency = dict(durationFrequency)
	newDurationList = []
	for key, value in durationFrequency.items():
		#coords = g.get_boundingbox_country(country=key, output_as='center')
		#add coords when solution is found
		entry = {"Duration":key}
		newDurationList.append(entry)
	write_list_of_dicts_to_csv(dkCfreqFile,newDurationList)

def logatFrequency():
	logatList = []
	for item in sessionList:
		logatList.append(item["Login"])
	logatFrequency = Counter(logatList)
	logatFrequency = dict(logatFrequency)
	newLogatyList = []
	for key, value in logatFrequency.items():
		#coords = g.get_boundingbox_country(country=key, output_as='center')
		#add coords when solution is found
		entry = {"Logins":key, "Frequency": value}
		newLogatList.append(entry)
	write_list_of_dicts_to_csv(logkCfreqFile,newlogatList)

# Writes our session list info to a CSV file
parseLog(logPath+logFile)
write_list_of_dicts_to_csv(outFile, sessionList)
countryFrequency()
durationFrequency()
logatFrequency()