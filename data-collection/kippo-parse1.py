import re
import csv
import pygeoip

# Helper function for string timestamp to int seconds
def get_sec(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

# Writes our log info to a csv file
def write_csv():
	out_file = open("test.csv","wb")
	fieldnames = sorted(list(set(k for d in sessionList for k in d)))
	writer = csv.DictWriter(out_file, fieldnames=fieldnames, dialect='excel')

	writer.writeheader()
	for row in sessionList:
	    writer.writerow(row)
	out_file.close()

gip = pygeoip.GeoIP("GeoIP.dat", pygeoip.MEMORY_CACHE)
gipc = pygeoip.GeoIP('GeoLiteCity.dat')

sessionList = []
x = 0
log = open(r"kippo.log", "r").read()

conn_list = re.split("(New connection:.*)",log)

for session in conn_list:
	
	print "-------- Session Start ---------"
	ip =  re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', session)
	if ip:
		ip = ip.pop(0)
	else:
		ip = 'none'
	
	la = re.findall("login attempt.*", session)
	for line in la:
		print "IP addr: " + ip  + "  \nLogin Attempts: " + line
	
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
		country = gip.country_name_by_addr(ip)
		records = gipc.record_by_addr(ip)
		country_name = records.get('country_name',None)
		country_code = records.get('country_code3',None)
		city = records.get('city',None)
	else:
		country_name = 'none'
		country_code = 'none'
		city = 'none'

	entry = {"ip":ip, "dur":duration, "log-at":la, "country name":country_name,"countr code":country_code , "city":city}
	sessionList.append(entry)

	print "-------- Session End ---------"


# Writes our session list info to a CSV file
write_csv()