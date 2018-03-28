import datetime
import os

glastopfStartPath = '../jmc/glastopf/financialfirstgroup/log/'
glastopfLogs = []

kippoStartPath = '../caw/kippo/kippo/log/'
kippoLogFile = 'kippo.log'
kippoLogs = []

startDate = "2018-03-09"
start = datetime.datetime.strptime(startDate, '%Y-%m-%d')
today = datetime.date.today()
end  = datetime.datetime(*(today.timetuple()[:3]))
step = datetime.timedelta(days=1)
while start < end:
	newPath = glastopfStartPath + '.' + start.strftime('%Y-%m-%d')
	start += step

kippoFilePath = '../caw/kippo/kippo/log/kippo.log'

def createSSHClient(server, port, user, password):
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(pm.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def generateAllGLogPaths():
	glastopfLogs.append(glastopfStartPath)
	startDate = "2018-03-09"
	start = datetime.datetime.strptime(startDate, '%Y-%m-%d')
	today = datetime.date.today()
	end  = datetime.datetime(*(today.timetuple()[:3]))
	step = datetime.timedelta(days=1)
	while start < end:
		newPath = glastopfStartPath + '.' + start.strftime('%Y-%m-%d')
		glastopfLogs.append(newPath)
		start += step

def generateAllKLogPaths():
	logPath = kippoStartPath+kippoLogFile
	kippoLogs.append(logPath)


	# TODO:
	# need a better way to figure out how many logs there are
	# also need to date these logs once they're processed
	
	for i in range(1,10):
		newPath = logPath + '.' + str(i)
		print newPath
		kippoLogs.append(newPath)


def getAllGlastopfLogs():
	os.chdir(glastopfStartPath)
	logs = [f for f in os.listdir() if os.isfile(os.join(mypath, f))]
	print logs

def getAllKippoLogs():
	generateAllKLogPaths()
	for log in kippoLogs:
		os.chdir('kippo/logs')
		scp.get(log)
		os.chdir('../../')

getAllGlastopfLogs()