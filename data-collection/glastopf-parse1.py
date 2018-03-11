import pygeoip
import requests

fileName = "glastopf.log"
gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)

activityList = []

def get_boundingbox_country(country, output_as='boundingbox'):
    """
    get the bounding box of a country in EPSG4326 given a country name

    Parameters
    ----------
    country : str
        name of the country in english and lowercase
    output_as : 'str
        chose from 'boundingbox' or 'center'. 
         - 'boundingbox' for [latmin, latmax, lonmin, lonmax]
         - 'center' for [latcenter, loncenter]

    Returns
    -------
    output : list
        list with coordinates as str
    """
    # create url
    url = '{0}{1}{2}'.format('http://nominatim.openstreetmap.org/search?country=',
                             country,
                             '&format=json&polygon=0')
    response = requests.get(url).json()[0]

    # parse response to list
    if output_as == 'boundingbox':
        lst = response[output_as]
        output = [float(i) for i in lst]
    if output_as == 'center':
        lst = [response.get(key) for key in ['lat','lon']]
        output = [float(i) for i in lst]
    return output

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
			coords = get_boundingbox_country(country=countryName, output_as='center')
			if requestedResource == "/": requestedResource = "index.html"

			entry = {"Date":date, "Timestamp":timeStamp, "IP":ipAddr, "Country":countryName, "Coords":coords, "StatusCode":httpStatusCode,"RequestMethod":httpRequestMethod,"Resource":requestedResource}
			print entry
			activityList.append(entry)



parseLog(fileName)