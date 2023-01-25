# IoT Ternium Project : Backend

## Napolitano

Napolitano is the API created by the IoT Semester I backend team in 2018, it can be accessed through the following IP:

> http://138.68.225.156:5000

To get information from the API, you should a GET request to any of the available routes with their respective parameters:

###### /login?nomina=&contrasena=
###### /insert?perfil=&nomina=&nombre=&mac=&grupo=&contrasena=&superusuario=
###### /showAll
###### /delete?nomina=
###### /search?nomina=
###### /searchGrupo?nomina=
###### /searchName?mac=
###### /modify?perfil=&nomina=&nombre=&mac=&grupo=
###### /record?mac=&floorid=&date=&hour=

It returns a flask.Response() and a status code 200. It could be transformed to a JSON with JSON.parse() 
The structure of the response depends on the parameters sent.
To know the JSON structure  you should see the comments in [vanilla/get_record.py](https://gitlab.com/semestreIOT/Backend/backend/blob/master /vanilla/get_record.py)

###### /danger?id_zone=&building=&floor=&data=

Save a risk zone in the database with the information provided, the id_zone must be unique and data must contain a number divisible by 4, example:

> /danger?id_zone=id_unico&building=ed1&floor=piso1&data=12.65 34.15 18.64 97.25


If the request is incomplete, the API will return an error message with a status code 400. Otherwise, it will return a status code 200 and with a "Done" message.

###### /getDanger?id_zone=

It returns a flask.Response() and a status code 200. It could be transformed to a JSON with JSON.parse() 
If an id_zone is given (and it exists), the information will maintain the following structure:
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
If an id_zone is not provided, the information is structured as follows:

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

Delete the risk zone with the given id

###### /modifyDanger?id_zone=&building=&floor=&data=

It modifies a risk zone with the given id, the id_zone, building, floor, and data parameters must be given (they must be divisible by 4) even if some of these data are not modified

## Vainilla
It modifies a risk zone with the given id, the id_zone, building, floor, and data parameters must be given (they must be divisible by 4) even if some of these data are not modified.

## Chocolate
SQL, MySQL Database, with information on workers, administrators, security personnel, etc.
