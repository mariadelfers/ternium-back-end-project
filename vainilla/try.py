import connect_db as mdb

def pnpoly(nvert, vertx, verty, testx, testy):
    i = 0
    j = nvert-1
    c = 0
    while (i < nvert):
        if ( ((verty[i]>testy) != (verty[j]>testy)) and (testx < (vertx[j]-vertx[i]) * (testy-verty[i]) / (verty[j]-verty[i]) + vertx[i]) ):
            c = not c 
        j = i
        i = i + 1
    return c

_, mydb = mdb.connect()

floor = "piso1"

cursor = mydb["dangerZones"].find({ "floor" : floor })

for document in cursor:
    vertx = []
    verty = []
    cont = True
    line = 0
    while(cont):
        if "line_" + str(line) in document:
            vertx.append(int(document["line_" + str(line)]["start_x"]))
            verty.append(int(document["line_" + str(line)]["start_y"]))
            line = line +1
        else:
            cont = False
    if (pnpoly(line, vertx, verty, 5, 2)):
        print("PELIGRO")

