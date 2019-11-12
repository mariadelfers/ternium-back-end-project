from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import hashlib

config = {
  'user': 'root',
  'passwd': '',
  'host': 'localhost',
  'database': 'chocolatee'
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
			args = (nomina, nombre, incriptado, superusuario)
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

	mycursor.callproc('MostrarT')
	row = mycursor.fetchone()
	empleados = {}
	trabajador = {}
	while row is not None:
		nomina = {}
		nomina["nombre"] = row[1]
		nomina["mac"] = row[4]
		trabajador[row[0]] = nomina
		row = mycursor.fetchone()

	empleados["trabajador"] = trabajador

	mycursor.callproc('MostrarS')
	row = mycursor.fetchone()
	supervisor = {}
	while row is not None:
		nomina = {}
		nomina["mac"] = row[4]
		nomina["nombre"] = row[1]
		supervisor[row[0]] = nomina
		row =  mycursor.fetchone()
	empleados["supervisor"] = supervisor

	mycursor.callproc('MostrarSeg')
	row = mycursor.fetchone()
	seguridad = {}
	while row is not None:
		nomina = {}
		nomina["nombre"] = row[1]
		seguridad[row[0]] = nomina
		row =  mycursor.fetchone()
	empleados["seguridad"] = seguridad

	mycursor.callproc('MostrarA')
	row = mycursor.fetchone()
	administrador = {}
	while row is not None:
		nomina = {}
		nomina["nombre"] = row[1]
		administrador[row[0]] = nomina
		row =  mycursor.fetchone()
	empleados["administrador"] = administrador

	return jsonify(empleados), 200

# Borrar de otras tablas
@app.route("/delete", methods=['GET'])
def Delete():

	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor()
	nomina = request.args.get('nomina')

	print(perfil, nomina)
	if(perfil == "trabajador"):
		sql = "DELETE FROM trabajador WHERE nomina_trabajador = %s"
	elif(perfil == "supervisor"):
		sql = "DELETE FROM supervisor WHERE nomina_supervisor= %s"
	elif(perfil == "administrador"):
		sql = "DELETE FROM administrador WHERE nomina_administrador = %s"
	elif(perfil == "seguridad"):
		sql = "DELETE FROM seguridad WHERE nomina_seguridad = %s"

	val = (nomina,)
	mycursor.execute(sql, val)
	# perfil = "Trabajador"
	if(mycursor.fetchone() is None):
		sql = "DELETE FROM supervisor WHERE nomina_supervisor = %s"
		val = (nomina,)
		mycursor.execute(sql, val)
		# perfil = "Supervisor"
		if(mycursor.fetchone() is None):
			sql = "DELETE * FROM administrador WHERE nomina_administrador = %s"
			val = (nomina, )
			mycursor.execute(sql, val)
			# perfil = "Administrador"
			if(mycursor.fetchone() is None):
				sql = "DELETE * FROM seguridad WHERE nomina_seguridad = %s"
				val = (nomina, )
				mycursor.execute(sql, val)
				# perfil = "Seguridad"

	print(mycursor.rowcount,"record deleted.")
	mydb.commit()

	return "."

#Dado una nomina
@app.route("/search", methods=['GET'])
def Search():

	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)
	nomina = request.args.get('nomina')

	val = (nomina,)
	mycursor.callproc('BuscarT', val)
	perfil = "Trabajador"
	if(mycursor.fetchone() is None):
		val = (nomina,)
		mycursor.callproc('BuscarS', val)
		perfil = "Supervisor"
		if(mycursor.fetchone() is None):
			val = (nomina, )
			mycursor.callproc('BuscarA', val)
			perfil = "Administrador"
			if(mycursor.fetchone() is None):
				val = (nomina, )
				mycursor.callproc('BuscarSeg', val)
				perfil = "Seguridad"

	row = mycursor.fetchone()
	nomina = {}
	if row is not None:
		nomina["nombre"] = row[1]
		nomina["perfil"] = perfil
		if perfil == "t" or perfil == "s":
			nomina["mac"] = row[4]

	print(mycursor.rowcount,"record founded.")
	return jsonify(nomina)

#Buscar un grupo dado un supervisor
@app.route("/searchGrupo", methods=['GET'])
def searchGrupo():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)
	nomina = request.args.get('nomina')

	val = (nomina, )
	mycursor.execute('BuscarGrupo', val)
	row = mycursor.fetchone()
	if(row is None):
		return "",401 #La nomina no existe
	else:
		return jsonify(row[5]), 200

# Dado una mac address
@app.route("/searchName", methods=['GET'])
def searchName():
	mydb = mysql.connector.connect(**config)
	mycursor = mydb.cursor(buffered=True)

	mac = request.args.get('mac')

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
	return jsonify(row[1])

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
		sql = "UPDATE trabajador SET nombre_trabajador = %s, mac_trabajador = %s, grupos_id_grupos = %s WHERE nomina_trabjador = %s"
		val = (nombre, mac, grupo, nomina )
		mycursor.execute(sql, val)
	elif(perfil == "supervisor"):
		sql = "UPDATE supervisor SET nombre_supervisor = %s, mac_supervisor = %s, grupos_id_grupos = %s WHERE nomina_supervisor = %s"
		val = (nombre, mac, grupo, nomina)
		mycursor.execute(sql, val)
	elif(perfil == "administrador"):
		sql = "UPDATE administrador SET nombre_administrador = %s WHERE nomina_administrador = %s"
		val = (nombre, nomina)
		mycursor.execute(sql, val)

	mydb.commit()
	return "", 200





if __name__ == '__main__':
	app.run()
