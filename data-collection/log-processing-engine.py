import os
import sched
import time

schedule = sched.scheduler(time.time, time.sleep)

def getCurrentLogs():
	print "Retrieving current logs..."
	os.system('python log-ret.py -allc')

def glastopf():
	print "Retrieving Glastopf logs..."
	os.system('python glastopf-parse2.py -today')
	print "Transfering Glastopf data..."
	os.system('python csv-transfer.py -g')

def amun():
	print "Retrieving Amun logs..."
	os.system('python amun-parse1.py -today')
	print "Transfering Amun data..."
	os.system('python csv-transfer.py -a')

def kippo():
	print "Retrieving Kippo logs..."
	os.system('python kippo-parse1.py -today')
	print "Transfering Kippo data..."
	os.system('python csv-transfer.py -k')
	
def runProcesses(sc):
	getCurrentLogs()
	glastopf()
	amun()
	#kippo()
	schedule.enter(120,1, runProcesses, (sc,))

if __name__ == '__main__':
	schedule.enter(1,1,runProcesses, (schedule,))
	schedule.run()