import pymongo 

def connect():
    myclient = pymongo.MongoClient('localhost', 27017)
    mydb = myclient.vainilla
    return myclient, mydb