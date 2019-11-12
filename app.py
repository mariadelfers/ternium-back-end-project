from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from flask_cors import CORS
import sys
from vainilla import get_record as gr
from vainilla import connect_db as mdb
import pymongo
import hashlib

config = {
  'user': 'BackEnd',
  'passwd': 'password',
  'host': 'localhost',
  'database': 'chocolate'
}

app = Flask(__name__)
CORS(app)


@app.route("/login", methods=['GET'])
def Login():
	mydb = mysql.connector.connect(**config)

	mycursor = mydb.cursor()
	nomina = request.args.get('nomina')
	contrasena = request.args.get('contrasena')

	salt="juanpi"+contrasena
	b=bytes(salt, "utf8")
	incriptado = hashlib.md5(b).hexdigest()


	mycursor = mydb.cursor()
	nomina = request.args.get('nomina')
	contrasena = request.args.get('contrasena')


	val = (nomina,)
	mycursor.callproc('LoginSupervisor', val)
	perfil = "Supervisor"
	row = list(mycursor.stored_results())[0].fetchall()
	a = True
	if(len(row)==0):
		val = (nomina, )
		mycursor.callproc('LoginAdministrador', val)
		perfil = "Administrador"
		row = list(mycursor.stored_results())[0].fetchall()
		if(len(row)==0):
			val = (nomina, )
			mycursor.callproc('LoginSeguridad', val)
			perfil = "Seguridad"
			row = list(mycursor.stored_results())[0].fetchall()
			if(len(row)==0):
				a = False

	print(row)
	if a:
		print(incriptado)
		if(row[0][2] == incriptado):
			return perfil, 200
	return "", 401


@app.route("/insert", methods=['GET'])
def Insert():
	mydb = mysql.connector.connect(**config)

	mycursor = mydb.cursor()
	perfil = request.args.get('perfil').lower()
	nomina = request.args.get('nomina')
	nombre = request.args.get('nombre')
	mac = request.args.get('mac')
	grupo = request.args.get('grupo')
	contrasena = request.args.get('contrasena')
	superusuario = request.args.get('superusuario')
	print("entra")

	salt="juanpi"+contrasena
	b=bytes(salt, "utf8")
	incriptado = hashlib.md5(b).hexdigest()

	if(perfil == "trabajador"):
		try:
			args = (nomina, nombre, grupo, mac)
			mycursor.callproc('InsertarT', args)
		except mysql.connector.IntegrityError:
			return "409"
	elif(perfil == "supervisor"):
		try:
			args = (nomina, nombre, incriptado, grupo, mac)
			mycursor.callproc('InsertarS', args)
		except mysql.connector.IntegrityError:
			return "409"
	elif(perfil == "administrador"):
		try:
			args = [nomina, nombre, incriptado, superusuario, ]
			mycursor.callproc('InsertarA', args)
		except mysql.connector.IntegrityError:
			return "409"
	elif(perfil == "seguridad"):
		try:
			args = (nomina, nombre, incriptado)
			mycursor.callproc('InsertarSeg', args)
			print("entro")
		except mysql.connector.IntegrityError:
			return "409"
	print("entro a insert")
	mydb.commit()
	print(mycursor.rowcount,"record inserted.")
	return "200"


@app.route("/showAll", methods=['GET'])
def ShowAll():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)

	empleados = {}

	mycursor.callproc("MostrarT", args=())
	row = list(mycursor.stored_results())[0].fetchall()
	trabajador = {}
	for data in row:
		nomina = {}
		nomina["nombre"] = data[1]
		nomina["mac"] = data[4]
		trabajador[data[0]] = nomina
	empleados["trabajador"] = trabajador

	mycursor.callproc("MostrarS", args=())
	row = list(mycursor.stored_results())[0].fetchall()
	supervisor = {}
	for data in row:
		nomina = {}
		nomina["nombre"] = data[1]
		nomina["mac"] = data[4]
		supervisor[data[0]] = nomina
	empleados["supervisor"] = supervisor

	mycursor.callproc("MostrarSeg", args=())
	row = list(mycursor.stored_results())[0].fetchall()
	seguridad = {}
	for data in row:
		nomina = {}
		nomina["nombre"] = data[1]
		seguridad[data[0]] = nomina
	empleados["seguridad"] = seguridad

	mycursor.callproc("MostrarA", args=())
	row = list(mycursor.stored_results())[0].fetchall()
	administrador = {}
	for data in row:
		nomina = {}
		nomina["nombre"] = data[1]
		administrador[data[0]] = nomina
	empleados["administrador"] = administrador

	return jsonify(empleados), 200

# Borrar de otras tablas
@app.route("/delete", methods=['GET'])
def Delete():

	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor()
	nomina = request.args.get('nomina')

	val = (nomina,)
	mycursor.callproc('EliminarTrabajador', val)
	mycursor.callproc('EliminarSupervisor', val)
	mycursor.callproc('EliminarAdministrador', val)
	mycursor.callproc('EliminarSeguridad', val)

	mydb.commit()

	return "."

@app.route("/search", methods=['GET'])
def Search():

	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)
	nomina = request.args.get('nomina')

	val = (nomina,)
	mycursor.callproc('BuscarT', val)
	perfil = "Trabajador"
	try:
		row = list(mycursor.stored_results())[0].fetchall()[0]
	except:
		val = (nomina,)
		mycursor.callproc('BuscarS', val)
		perfil = "Supervisor"
		try:
			row = list(mycursor.stored_results())[0].fetchall()[0]
		except:
			val = (nomina, )
			mycursor.callproc('BuscarA', val)
			perfil = "Administrador"
			try:
				row = list(mycursor.stored_results())[0].fetchall()[0]
			except:
				val = (nomina, )
				mycursor.callproc('BuscarSeg', val)
				perfil = "Seguridad"
				try:
					row = list(mycursor.stored_results())[0].fetchall()[0]
				except:
					row = None

	nomina = {}
	if row is not None:
		nomina["nomina"] = row[0]
		nomina["nombre"] = row[1]
		nomina["perfil"] = perfil
		if perfil == "Trabajador" or perfil == "Supervisor":
			nomina["mac"] = row[2]
			nomina["grupo"] = row[3]

	print(mycursor.rowcount,"record founded.")
	return jsonify(nomina)

@app.route("/searchGrupo", methods=['GET'])
def searchGrupo():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)
	nomina = request.args.get('nomina')

	val = (nomina, )
	mycursor.callproc('BuscarGrupo', val)
	try:
		row = list(mycursor.stored_results())[0].fetchall()
	except:
		row = None

	if(row is None):
		return "",401 #La nomina no existe
	else:
		return jsonify(row[0]), 200

# Dado una mac address
@app.route("/searchName", methods=['GET'])
def searchName():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)

	mac = request.args.get('mac')

	val = (mac,)
	mycursor.callproc('BuscarNombreT', val)
	try:
		row = list(mycursor.stored_results())[0].fetchall()
	except:
		val = (mac,)
		mycursor.callproc('BuscarNombreS', val)
		try:
			row = list(mycursor.stored_results())[0].fetchall()
		except:
			row = None
	if(row is None):
		return "", 401 #La Mac Address no existe
	print(mycursor.rowcount,"record founded.")
	return jsonify(row[0]),200

@app.route("/crearGrupo", methods=['GET'])
def crearGrupo():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)
	idgrupo = request.args.get('idgrupo')
	zona = request.args.get('zona')

	val = (idgrupo, zona, )
	mycursor.callproc('CrearGrupo', val)
	return "",200

@app.route("/borrarGrupo", methods=['GET'])
def borrarGrupo():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)
	idgrupo = request.args.get('idgrupo')

	val = (idgrupo, )
	mycursor.callproc('BorrarGrupo', val)
	return "",200

@app.route("/modificarGrupo", methods=['GET'])
def modificarGrupo():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)
	idgrupo = request.args.get('idgrupo')
	zona = request.args.get('zona')

	val = (idgrupo, zona)
	mycursor.callproc('ModificarGrupo', val)
	return "",200

@app.route("/modify", methods=['GET'])
def modify():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)

	perfil = request.args.get('perfil').lower()
	nomina = request.args.get('nomina')
	nombre = request.args.get('nombre')
	mac = request.args.get('mac')
	grupo = request.args.get('grupo')

	if(perfil == "trabajador"):
		val = (nomina, nombre, mac, grupo)
		mycursor.callproc('ActualizarTrabajador', val)
	elif(perfil == "supervisor"):
		val = (nomina, nombre, mac, grupo)
		mycursor.callproc('ActualizarSupervisor', val)
	elif(perfil == "seguridad"):
		val = (nomina, nombre)
		mycursor.callproc('ActualizarSeguridad', val)
	elif(perfil == "administrador"):
		val = (nomina, nombre)
		mycursor.callproc('ActualizarAdministrador', val)

	mydb.commit()
	return "", 200

# http://localhost:5000/record?mac=&floorid=&date=&hour=
@app.route("/record", methods=['GET'])
def record():
        mac = request.args.get('mac')
        floor_id = request.args.get('floorid')
        date = request.args.get('date')
        hour = request.args.get('hour')
        function = int(str(int(mac is not None)) +  str(int(floor_id is not None)) +  str(int(date is not None)) + str(int(hour is not None)), 2)

        if function == 1:
                return jsonify(gr.get_record_with_hour(hour))
        elif function == 2:
                return jsonify(gr.get_record_with_date(date))
        elif function == 3:
                return jsonify(gr.get_record_with_date_and_hour(date, hour))
        elif function == 4:
                return jsonify(gr.get_record_with_floorid(floor_id))
        elif function == 5:
                return jsonify(gr.get_record_with_floorid_and_hour(floor_id, hour))
        elif function == 6:
                return jsonify(gr.get_record_with_floorid_and_date(floor_id, date))
        elif function == 7:
                return jsonify(gr.get_record_with_floorid_date_and_hour(floor_id, date, hour))
        elif function == 8:
                return jsonify(gr.get_record_with_mac(mac))
        elif function == 9:
                return jsonify(gr.get_record_with_mac_and_hour(mac, hour))
        elif function == 10:
                return jsonify(gr.get_record_with_mac_and_date(mac, date))
        elif function == 11:
                return jsonify(gr.get_record_with_mac_date_and_hour(mac, date, hour))
        elif function == 12:
                return jsonify(gr.get_record_with_mac_and_floorid(mac, floor_id))
        elif function == 13:
                return jsonify(gr.get_record_with_mac_floorid_and_hour(mac, floor_id, hour))
        elif function == 14:
                return jsonify(gr.get_record_with_mac_floorid_and_date(mac, floor_id, date))
        elif function == 15:
                return jsonify(gr.get_record_with_mac_floorid_date_and_hour(mac, floor_id, date, hour))

@app.route("/realtime", methods=['GET'])
def real_time():
	response = gr.get_record_real_time()
	for floor in response:
		for mac in response[floor]:
			name,_ = searchNameWithMac(response[floor][mac]['_id'])
			response[floor][mac]['_id'] = name
	return jsonify(response)

@app.route("/danger", methods=['GET'])
def danger():
	_, mydb = mdb.connect()

	id_zone = request.args.get('id_zone')
	building = request.args.get('building')
	floor = request.args.get('floor')
	data = request.args.get('data')

	if id_zone is None or building is None or floor is None or data is None:
		print(id_zone)
		print(building)
		print(floor)
		print(data)
		return "Error in given data", 400

	data = data.split(" ")

	if len(data) % 4 != 0:
		return "Error in given data", 400

	zone_db = mydb["dangerZones"]
	zone_data = {
		"_id" : id_zone,
		"floor" : floor,
		"building" : building
	}

	for i in range(0, len(data), 4):
		line = {
			"start_x" : data[i],
			"start_y" : data[i + 1],
			"end_x" : data[i + 2],
			"end_y" : data[i + 3]
		}
		zone_data["line_" + str(i // 4)] = line
	try:
		zone_db.insert_one(zone_data)
	except:
		return "Zone already exists", 400
	return "Done", 200

@app.route("/getDanger", methods=['GET'])
def get_danger_zones():
	_, mydb = mdb.connect()

	id_zone = request.args.get('id_zone')
	if id_zone is None:
		cursor = mydb["dangerZones"].find({})
		zones = {}
		for document in cursor:
			zones[document["_id"]] = document
		return jsonify(zones)
	else:
		return jsonify(mydb["dangerZones"].find_one({"_id" : id_zone}))

@app.route("/delDanger", methods=['GET'])
def delete_danger_zone():
	_, mydb = mdb.connect()
	id_zone = request.args.get('id_zone')

	mydb["dangerZones"].delete_one({"_id" : id_zone})

	return "Done", 200

@app.route("/modifyDanger", methods=['GET'])
def modyfy_danger_zone():
	_, mydb = mdb.connect()

	id_zone = request.args.get('id_zone')
	building = request.args.get('building')
	floor = request.args.get('floor')
	data = request.args.get('data')

	if id_zone is None or building is None or floor is None or data is None:
		print(id_zone)
		print(building)
		print(floor)
		print(data)
		return "Error in given data", 400

	data = data.split()

	if len(data) % 4 != 0:
		return "Error in given data", 400

	zone_data = {
		"_id" : id_zone,
		"floor" : floor,
		"building" : building
	}

	for i in range(0, len(data), 4):
		line = {
			"start_x" : data[i],
			"start_y" : data[i + 1],
			"end_x" : data[i + 2],
			"end_y" : data[i + 3]
		}
		zone_data["line_" + str(i)] = line

	mydb["dangerZones"].find_one_and_update({"_id": id_zone},
                                 {"$set": zone_data})

	return "Done", 200

@app.route("/")
def main():
    return "<h1>Move along, Nothing to see here</h1>"


def searchNameWithMac(mac):
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)

	sql = "SELECT * FROM trabajador WHERE mac_trabajador = %s"
	val = (mac,)
	mycursor.execute(sql, val)
	row = mycursor.fetchone()
	if(row is None):
		sql = "SELECT * FROM supervisor WHERE mac_supervisor = %s"
		val = (mac,)
		mycursor.execute(sql, val)
		row = mycursor.fetchone()
		if(row is None):
			return "", 401 #La Mac Address no existe
	print(mycursor.rowcount,"record founded.")
	return row[1],200

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
