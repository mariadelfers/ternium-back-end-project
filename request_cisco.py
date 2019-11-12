import pymongo
import requests
import time
from vainilla import connect_db

def getRealTimeLocation():
        localtime = time.localtime(time.time())
        m = str(localtime[1]) if localtime[1] > 9 else '0' + str(localtime[1])
        sec = '00' if localtime[5] < 30 else '30'
        mins = str(localtime[4]) if localtime[4] > 9 else '0' + str(localtime[4])
        hour = str(localtime[3]) if localtime[3] > 9 else '0' + str(localtime[3])
        formatTime = hour + ':' + mins + ':' + sec
        formatDate = m + '/' + str(localtime[2]) + '/' + str(localtime[0])
        return formatDate + '-' + formatTime

#mydb = pymongo.MongoClient('mongodb://localhost:27017/ternium').vainilla
_,mydb = connect_db.connect()

while 1:
	r = requests.get('http://10.190.154.230/api/location/v3/clients', auth=('cmxapi', 'Cmx4p1'))

	for client in r.json():
		print (client['deviceId'])
		print ([client['locationCoordinate']['x'],client['locationCoordinate']['y']])

		collection = mydb[client['locationMapHierarchy']]
		doc = collection.find_one({'_id':client['deviceId']})
		try:
			realTime = getRealTimeLocation()
			doc[realTime] = [client['locationCoordinate']['x'],client['locationCoordinate']['y']]
			mydb[client['locationMapHierarchy']].update({'_id':client['deviceId']},doc)
			doc = collection.find_one({'_id':client['deviceId']})
			print (doc[realTime])

		except Exception as e:
			print (e)
			print ("None")
