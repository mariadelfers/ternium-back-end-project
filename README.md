# Backend

## Napolitano

Napolitano es la API creada por el equipo de backend del Semestre I de IoT 2018, se puede acceder a ella por medio de la siguiente IP:

> http://138.68.225.156:5000

Para obtener informacion de la API se debe de realizar una peticion GET hacia cualquiera de las rutas disponibles con sus respectivos parametros:

###### /login?nomina=&contrasena=
###### /insert?perfil=&nomina=&nombre=&mac=&grupo=&contrasena=&superusuario=
###### /showAll
###### /delete?nomina=
###### /search?nomina=
###### /searchGrupo?nomina=
###### /searchName?mac=
###### /modify?perfil=&nomina=&nombre=&mac=&grupo=
###### /record?mac=&floorid=&date=&hour=

Regresa un flask.Response() y un status code 200. Se puede convertir en un JSON con JSON.parse(); la estructura de la respuesta depende de los parametros que se den, para saber la estructura del JSON se deben ver los comentarios en [vainilla/get_record.py](https://gitlab.com/semestreIOT/Backend/backend/blob/master/vainilla/get_record.py)

###### /danger?id_zone=&building=&floor=&data=

Guarda una zona de riesgo en la base de datos con la informacion proporcionada, el id_zone debe ser unico y data debe de contener un numero divisible entre 4, ej: 

> /danger?id_zone=id_unico&building=ed1&floor=piso1&data=12.65 34.15 18.64 97.25

En caso que no se proporcione alguno de los parametros o que alguna de estas condiciones no se cumpla se regresara un mensaje con el tipo de error y un status code 400, de lo contrario se regresara un status code 200 con un mensaje de "Done"

###### /getDanger?id_zone=

Regresa un flask.Response() y un status code 200. Se puede convertir en un JSON con JSON.parse(); en caso que se de un id_zone (y que este exista) la informacion mantendra la siguiente estructura:

```
{
    _id : id_zoneX,
    floor : floorX,
    building : buildingX,
    line_X : {
        start_x : data,
        start_y :data,
        end_x : data,
        end_y : data
    }
}
```

Si no se proporciona un id_zone la informacion estara estructurada de la siguiente manera:

```
{
    id_zoneX : {
        _id : id_zoneX,
        floor : floorX,
        building : buildingX,
        line_X : {
            start_x : data,
            start_y :data,
            end_x : data,
            end_y : data
        }
    }
    id_zoneY : { ... }
    id_zoneZ : { ... }
}
```

###### /delDanger?id_zone=

Borra la zona de riesgo con el id dado

###### /modifyDanger?id_zone=&building=&floor=&data=

Modifica la zona de riesgo con el id dado, se tienen que dar los parametros id_zone, building, floor, data (deben ser divisible entre 4) aun cuando alguno de estos datos no se modifiquen.


## Vainilla

Base de Datos NoSQL, MongoDB, en donde se guarda información en tiempo real de ubicación de los trabajadores, alertas generadas y zonas de riesgo.

## Chocolate

Base de Datos SQL, MySQL, con información de los trabajadores, administradores, personal de seguridad, etc.