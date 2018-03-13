import pygeoip
import getCenterCords as g
import csv
from collections import Counter
import os

fileName = "glastopf.log"
outFile = "glastopf.csv"
allLog = "all.csv"
gCfreqFile = "gcf.csv"
logPath = "glastopf/logs/"
csvPath = "glastopf/csv/"
gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)
ignoreLine = ["Initializing Glastopf","Connecting to main database", "Glastopf started", "Bootstrapping dork database","Generating initial dork pages","Stopping Glastopf"]

activityList = []

def write_list_of_dicts_to_csv(fileName, list_of_dicts):
	os.chdir('glastopf/csv')
	print activityList
	with open(fileName,"wb") as out_file:
		fieldnames = sorted(list(set(k for d in list_of_dicts for k in d)))
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writeheader()
		for row in list_of_dicts:
		    writer.writerow(row)
		os.chdir('../../')

def write_dict_to_csv(fileName,fieldNames, myDict):
	os.chdir('glastopf/csv')
	with open(fileName,"wb") as out_file:
		fieldnames = fieldNames
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writer.writerow
		for key, value in myDict.items():
			writer.writerow([key, value])

def getAllLogs():
	os.chdir('glastopf/logs')
	logs = os.listdir('.')
	os.chdir('../../')
	return logs

def parseLog(fileName):
	print "Filename: " + fileName
	with open(fileName, "r") as file:
		for line in file:
			if any(x in line for x in ignoreLine):
				pass
				print "Pass"
			else:	
				contents = line.split()
				print "Contents" + str(contents)
				date = contents[0]
				secondGroup = contents[1].split(",")
				timeStamp = secondGroup[0]
				httpStatusCode = secondGroup[1]
				ipAddr = contents[3]
				httpRequestMethod = contents[5]
				requestedResource = contents[6]
				countryName =  gip.country_name_by_addr(ipAddr)
				#coords = g.get_boundingbox_country(country=countryName, output_as='center')
				if requestedResource == "/": requestedResource = "index.html"

				#add coords back to dict when possible
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
		entry = {"Country":key,"Frequency":value}
		newCountryList.append(entry)
	write_list_of_dicts_to_csv(gCfreqFile,newCountryList)	

#parseLog(fileName)
write_list_of_dicts_to_csv(outFile,activityList)
parseAllLogs()
countryFrequency()