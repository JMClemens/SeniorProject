import pygeoip
import getCenterCords as g

fileName = "glastopf.log"
gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)

activityList = []

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