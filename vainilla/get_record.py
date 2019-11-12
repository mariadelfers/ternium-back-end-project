import pymongo
from vainilla import connect_db as mdb
import time

# Return:
# {
#       "id_floorX" : {
#               "macX" : {
#                       "_id" = "macX"
#                       "date-time" : [x, y]
#               }
#       }
# }
def get_record_with_hour(hour):
        _, mydb = mdb.connect()
        record_dict = {}
        for collection in mydb.list_collection_names():
                collection_data = {}
                cursor = mydb[collection].find({})
                for document in cursor:
                        document_data = {}
                        for key, value in document.items():
                                if hour in key:
                                        document_data["_id"] = document["_id"]
                                        document_data[key] = value
                        if document_data:
                                collection_data[document_data["_id"]] = document_data
                if collection_data:
                        record_dict[collection] = collection_data
        return record_dict

# Return:
# {
#       "id_floorX" : {
#               "macX" : {
#                       "_id" = "macX"
#                       "date-time" : [x, y]
#               }
#       }
# }
def get_record_with_date(date):
        return get_record_with_hour(date)

# Return:
# {
#       "id_floorX" : {
#               "macX" : {
#                       "_id" = "macX"
#                       "date-time" : [x, y]
#               }
#       }
# }
def get_record_with_date_and_hour(date, hour):
        _, mydb = mdb.connect()
        record_dict = {}
        for collection in mydb.list_collection_names():
                collection_data = {}
                cursor = mydb[collection].find({ date + "-" + hour : { "$exists" : True }})
                for document in cursor:
                        document_data = {}
                        document_data["_id"] = document["_id"]
                        document_data[date + "-" + hour] = document[date + "-" + hour]
                        if document_data:
                                collection_data[document_data["_id"]] = document_data
                if collection_data:
                        record_dict[collection] = collection_data
        return record_dict

# Return:
# {
#        "macX" : {
#                 "_id" = "macX"
#                 "date-time" : [x, y]
#         }
# }
def get_record_with_floorid(floor_id):
        _, mydb = mdb.connect()
        record_dict = {}
        cursor = mydb[floor_id].find({})
        for document in cursor:
                record_dict[document["_id"]] = document
        return record_dict

# Return:
# {
#        "macX" : {
#                 "_id" = "macX"
#                 "date-time" : [x, y]
#         }
# }
def get_record_with_floorid_and_hour(floor_id, hour):
        _, mydb = mdb.connect()
        record_dict = {}
        cursor = mydb[floor_id].find({})
        for document in cursor:
                collection_data = {}
                for key, value in document.items():
                        if hour in key:
                                collection_data[key] = value
                                collection_data["_id"] = document["_id"]
                if collection_data:
                        record_dict[document["_id"]] = collection_data
        return record_dict

# Return:
# {
#        "macX" : {
#                 "_id" = "macX"
#                 "date-time" : [x, y]
#         }
# }
def get_record_with_floorid_and_date(floor_id, date):
        return get_record_with_floorid_and_hour(floor_id, date)

# Return:
# {
#        "macX" : {
#                 "_id" = "macX"
#                 "date-time" : [x, y]
#         }
# }
def get_record_with_floorid_date_and_hour(floor_id, date, hour):
        _, mydb = mdb.connect()
        record_dict = {}
        cursor = mydb[floor_id].find({date + "-" + hour : { "$exists" : True } })
        for document in cursor:
                collection_data = {}
                collection_data["_id"] = document["_id"]
                collection_data[date + "-" + hour] = document[date + "-" + hour]
                record_dict[document["_id"]] = collection_data
        return record_dict

# Return:
# {
#       id_floorX : {
#               "_id" = "id_floorX"
#               "date-time" : [x, y]
#       }
# }
def get_record_with_mac(mac):
        _, mydb = mdb.connect()
        record_dict = {}
        for collection in mydb.list_collection_names():
                collection_data = mydb[collection].find_one({"_id" : mac})
                if collection_data:
                        collection_data["_id"] = collection
                        record_dict[collection] = collection_data
        return record_dict

# Return:
# {
#       id_floorX : {
#               "_id" = "id_floorX"
#               "date-time" : [x, y]
#       }
# }
def get_record_with_mac_and_hour(mac, hour):
        _, mydb = mdb.connect()
        record_dict = {}
        for collection in mydb.list_collection_names():
                collection_data = {}
                for key, value in mydb[collection].find_one({"_id" : mac}).items():
                        if hour in key:
                                collection_data[key] = value
                if collection_data:
                        collection_data["_id"] = collection
                        record_dict[collection] = collection_data
        return record_dict

# Return:
# {
#       id_floorX : {
#               "_id" = "id_floorX"
#               "date-time" : [x, y]
#       }
# }
def get_record_with_mac_and_date(mac, date):
        return get_record_with_mac_and_hour(mac, date)

# Return:
# {
#       id_floorX : {
#               "_id" = "id_floorX"
#               "date-time" : [x, y]
#       }
# }
def get_record_with_mac_date_and_hour(mac, date, hour):
        _, mydb = mdb.connect()
        record_dict = {}
        for collection in mydb.list_collection_names():
                collection_data = mydb[collection].find_one({"_id" : mac})
                if date + "-" + hour in collection_data:
                        data = collection_data[date + "-" + hour]
                        collection_data = {}
                        collection_data[collection] = data
                else:
                        collection_data = {}
                if collection_data:
                        collection_data["_id"] = collection
                        record_dict[collection] = collection_data
        return record_dict

# Return:
# {
#        "_id" = "macX"
#        "date-time" : [x, y]
# }
def get_record_with_mac_and_floorid(mac, floor_id):
        _, mydb = mdb.connect()
        record_dict = {}
        record_dict = mydb[floor_id].find_one({"_id" : mac})
        return record_dict

# Return:
# {
#        "_id" = "macX"
#        "date-time" : [x, y]
# }
def get_record_with_mac_floorid_and_hour(mac, floor_id, hour):
        _, mydb = mdb.connect()
        record_dict = {}
        for key, value in mydb[floor_id].find_one({"_id" : mac}).items():
                if hour in key:
                        record_dict[key] = value
        return record_dict

# Return:
# {
#        "_id" = "macX"
#        "date-time" : [x, y]
# }
def get_record_with_mac_floorid_and_date(mac, floor_id, date):
        return get_record_with_mac_floorid_and_hour(mac, floor_id, date)

# Return:
# {
#        "date-time" : [x, y]
# }
def get_record_with_mac_floorid_date_and_hour(mac, floor_id, date, hour):
        _, mydb = mdb.connect()
        record_dict = {}
        record_dict[date + "-" + hour] = mydb[floor_id].find_one({"_id" : mac})[date + "-" + hour]
        return record_dict

def get_record_real_time():
        localtime = time.localtime(time.time())
        m = str(localtime[1]) if localtime[1] > 9 else '0' + str(localtime[1])
        sec = '00' if localtime[5] < 30 else '30'
        mins = str(localtime[4]) if localtime[4] > 9 else '0' + str(localtime[4])
        hour = str(localtime[3]) if localtime[3] > 9 else '0' + str(localtime[3])
        formatTime = hour + ':' + mins + ':' + sec
        formatDate = m + '/' + str(localtime[2]) + '/' + str(localtime[0])
        return get_record_with_date_and_hour(formatDate,formatTime)

# print(get_record_with_mac_floorid_date_and_hour(mac="mac0", floor_id="id_piso1", date="05/11/2018", hour="14:09:00")
