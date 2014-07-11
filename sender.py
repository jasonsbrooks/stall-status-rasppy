import requests
import datetime
from pyk8055 import *
from time import sleep

now = datetime.datetime.utcnow

def sendUpdate(stallNum, newState):
	print 'sending an update! ', stallNum, newState
	reqType = 'open' if newState == 1 else 'close'
	payload = {'stall_num': stallNum, 'room_id': '53befa251f0070ada694db70'}
	r = requests.post("http://stall-status.herokuapp.com/stalls/%s" %(reqType), data=payload)
	print r.content

try:
	k = k8055(0)
	numstalls = 2
	changeTimes = [now() for i in range(numstalls)]
	changed = [False for i in range(numstalls)]
	state = [k.ReadDigitalChannel(i + 1) for i in range(numstalls)]
	while(1):
		for i in range(numstalls):
			r = k.ReadDigitalChannel(i + 1)
			# print 'stall {}: {}'.format(i, r)
			if r != state[i] and not changed[i]:
				print 'observing new change'
				changeTimes[i] = now()
				changed[i] = True
				state[i] = r
			elif r == state[i] and changed[i] and now() - changeTimes[i] > datetime.timedelta(seconds=0.5):
				sendUpdate(i, state[i])
				changed[i] = False
				changeTimes[i] = now()

except IOError:
	print "Could not open device"

