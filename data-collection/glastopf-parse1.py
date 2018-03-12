import pygeoip
import getCenterCords as g
import csv
from collections import Counter

fileName = "glastopf/logs/glastopf.log"
outFile = "glastopf/csv/glastopf.csv"
gCfreqFile = "glastopf/csv/gcf.csv"
gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)

activityList = []

def write_list_of_dicts_to_csv(fileName, list_of_dicts):
	with open(fileName,"wb") as out_file:
		fieldnames = sorted(list(set(k for d in list_of_dicts for k in d)))
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writeheader()
		for row in list_of_dicts:
		    writer.writerow(row)

def write_dict_to_csv(fileName,fieldNames, myDict):
	with open(fileName,"wb") as out_file:
		fieldnames = fieldNames
		writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')
		writer.writer.writerow
		for key, value in myDict.items():
			writer.writerow([key, value])


def parseLog(fileName):
	with open(fileName, "r") as file:
		for line in file:
			if "Initializing Glastopf" or "Connecting to main database" or "Glastopf started" in line:
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
				#coords = g.get_boundingbox_country(country=countryName, output_as='center')
				if requestedResource == "/": requestedResource = "index.html"

				#add coords back to dict when possible
				entry = {"Date":date, "Timestamp":timeStamp, "IP":ipAddr, "Country":countryName, "StatusCode":httpStatusCode,"RequestMethod":httpRequestMethod,"Resource":requestedResource}
				#print entry
				activityList.append(entry)

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

parseLog(fileName)
write_list_of_dicts_to_csv(outFile,activityList)
countryFrequency()