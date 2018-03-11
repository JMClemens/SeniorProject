import pygeoip
import getCenterCords as g

fileName = "glastopf.log"
outFile = "glastopf.csv"
gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)

activityList = []

def write_csv(fileName):
	out_file = open(fileName,"wb")
	fieldnames = sorted(list(set(k for d in activityList for k in d)))
	writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')

	writer.writeheader()
	for row in activityList:
	    writer.writerow(row)
	out_file.close()

def parseLog(fileName):
	with open(fileName, "r") as file:
		for line in file:
			contents = line.split()

			date = contents[0]
			secondGroup = contents[1].split(",")
			timeStamp = secondGroup[0]
			httpStatusCode = secondGroup[1]
			ipAddr = contents[3]
			httpRequestMethod = contents[5]
			requestedResource = contents[6]
			countryName =  gip.country_name_by_addr(ipAddr)
			coords = g.get_boundingbox_country(country=countryName, output_as='center')
			if requestedResource == "/": requestedResource = "index.html"

			entry = {"Date":date, "Timestamp":timeStamp, "IP":ipAddr, "Country":countryName, "Coords":coords, "StatusCode":httpStatusCode,"RequestMethod":httpRequestMethod,"Resource":requestedResource}
			print entry
			activityList.append(entry)



parseLog(fileName)
write_csv(outFile)