# VAINILLA

## Base de datos no relacional para el proyecto del Semestre I IoT 2018

### Requisitos:

* [Python](https://www.python.org/downloads/)
* [MongoDB](https://www.mongodb.com/download-center/community)
* [PyMongo](https://api.mongodb.com/python/current/installation.html)
* [Flask](http://flask.pocoo.org/)
* [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
* [MySQL-Connector](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)


### Descripción de archivos:

#### fill_database.py

Llena una BD de Mongo con datos falsos:
  * Historial de x trabajadores por un año
  * Notificaciones de x trabajadores por un año
  * X zonas de riesgo

#### flask_get_record.py

Genera una app con flask con rutas para realizar busquedas al historial de los trabajadores
Rutas:
1. /record?mac=&floorid=&date=&hour=
  * Los parametros (mac, floorid, date y hour) son opcionales dependiendo de lo que se quiera buscar
  * mac = mac que se quiere buscar
  * floorid = id del piso que se quiere buscar
  * date = fecha en la cual se quiere buscar
  * hout = hora de la cual se quiere buscar

#### get_record.py

Busquedas del historial de los usuaios hacia la base de datos de mongo

#### index.html

Ejemplo de como realizar requests hacia la pagina generada por *flask_get_record.py*

#### mysql_connection.py

Ejemplo de como realizar una conexión a MySQL en python