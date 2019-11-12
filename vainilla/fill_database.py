import pymongo
import datetime

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["vainilla"]

###################################################################################

# Simulando datetime.datetime.now().strftime('%m/%d/%Y-%H:%M:%S')
timestamp = []
for month in range(1, 11):
        if month < 10:
                month = "0" + str(month)
        month = str(month)
        for day in range(1, 31):
                if day < 10:
                        day = "0" + str(day)
                day = str(day)
                for hour in range(24):
                        if hour < 10:
                                hour = "0" + str(hour)
                        hour = str(hour)
                        for minutes in range(60):
                                if minutes < 10:
                                        minutes = "0" + str(minutes)
                                for seconds in range(2):
                                        second = "30"
                                        if seconds == 0:
                                                second = "00"
                                        minutes = str(minutes)
                                        timestamp.append("%s/%s/2018-%s:%s:%s"%(month, day, hour, minutes, second))

####################################################################################

# Pruebas para zonas de riesgo
# Cuadrados por zona de riesgo
squares = 6
# Numero de zonas de riesgo
dangerZones = 3

dangerZone = mydb["dangerZones"]

for zones in range(dangerZones):
        zone = { "_id" : "zona" + str(zones)}
        for square in range(squares):
                zone["square" + str(square)] = [123.456, 123.456, 123.456, 123.456]

        dangerZone.insert_one(zone)

####################################################################################
import requests

persons = []
floors = []

r = requests.get('http://cmxlocationsandbox.cisco.com/api/location/v2/clients', auth=('learning', 'learning'))
for client in r.json():
        persons.append(client['macAddress'])

r = requests.get('http://cmxlocationsandbox.cisco.com/api/config/v1/maps/floor/list', auth=('learning', 'learning'))
for floor in r.json():
        floors.append(floor)

floors.append('piso1')
floors.append('piso2')

# Pruebas de historial de macs
# Deberia ser 20
num_floors = len(floors)
# Deberia ser 2000

buildings = []
for floor in floors:
        buildings.append(mydb[str(floor)])

for person in persons:
        print (person)
        index_timestamp = 0
        for building in buildings:
                history = { "_id" : str(person) }
                for time in range(int(len(timestamp) // num_floors)):
                        history[timestamp[index_timestamp]] = [123.456, 654.321]
                        index_timestamp += 1
                building.insert_one(history)

#####################################################################################

# Pruebas de notificaciones
# Deberia ser 2000
persons = 3
num_floors = 5

notifications = mydb["notifications"]

# Deberian ser 2000
for person in range(persons):
        history = { "_id" : "mac" + str(person)}
        timestamp_index = 0
        for floor in range(num_floors):
                for time in range(len(timestamp) // num_floors):
                        history[timestamp[timestamp_index]] = [123.456, 123.456, "id_piso" + str(floor)]
                        timestamp_index += 1

        notifications.insert_one(history)

#####################################################################################
