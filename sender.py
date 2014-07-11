import requests

def sendUpdate(stallNum, reqType):
	payload = {'stall_num': stallNum, 'room_id': '53befa251f0070ada694db70'}
	r = requests.post("http://10.4.106.210:3000/stalls/%s" %(reqType), data=payload)
	print r.content

