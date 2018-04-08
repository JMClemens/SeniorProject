import pycountry
import getCenterCords as g
import time
import csv

countryList = []

def write_csv():
	out_file = open("coords.csv","wb")
	fieldnames = sorted(list(set(k for d in countryList for k in d)))
	writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')

	writer.writeheader()
	for row in countryList:
	    writer.writerow(row)
	out_file.close()

for item in pycountry.countries:
	if(item.name == "Hong Kong"): codeCheck = "China"
	elif(item.name == "Korea, Republic of"): codeCheck = "Korea"
	else: codeCheck = item.name
	coords = g.get_boundingbox_country(country=codeCheck, output_as='center')
	time.sleep(2)
	print codeCheck
	item = {"Country":codeCheck,"Coords":coords}

	countryList.append(item)

write_csv()
