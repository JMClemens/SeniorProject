import re

sessionList = []
x = 0
log = open(r"kippo.log", "r").read()

conn_list = re.split("New connection:.*",log)

for session in conn_list:
	x = x + 1
	print "----------- New Session --------"
	ip =  re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', session)
	set(ip)
	for i in ip:
		print "Ip item: " + i
	la = re.findall("login attempt.*",session);
	for bl in ip:
		for line in la:
			print "Run num: " + str(x) + " \nIP addr: " + bl + "  \nLogin Attempts: " + line
