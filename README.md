# 4.-Creating-an-API

![Image](https://miro.medium.com/max/900/1*5SX4nfBJHkVXEA13dfoQ3w.png)

# Overview

El objetivo de este proyecto es por un lado, crear una API cuyos endpoints inserten datos en una base de datos de mongodb, y por otro analizar la sensación general de esos datos.

# Objetivos

* Crear una API en flask que inserten mensajes de texto en una database de mongodb.
* Extraer el sentimiento individual de cada mensaje de un chat y devolver el sentimiento general del chat.


# Instrucciones

Para ir insertando datos en la base de datos de mongodb se van cambiando los endpoints (extensiones) de nuestra API. 

## Crear un usuario

`/user/create/<username>`

Si el nombre de usuario ya existe, no dejará introducirlo en la base de datos.

url = http://localhost:5000/user/create/Jesse
res = requests.get(url)


## Crear un chat

`/chat/create/<chatname>`

Esta extensión de la URL devuelve un json con el id del chat en mongodb y el nombre del chat. Si no se inserta correctalmente la url entre otras cosas, devolverá un error. Además si el nombre del chat ya existe, no dejará introducirlo de nuevo.

url = http://localhost:5000/chat/create/BeforeSunrise
res = requests.get(url)


## Añadir un usuario a un chat

`/chat/<chatname>/adduser/<user>`

Solo se podrá añadir el usuario un chat si tanto el usuario como el chat existen previamente.


url = http://localhost:5000/chat/BeforeSunrise/adduser/Jesse
res = requests.get(url)


## Insertar un mensaje en un chat

`/chat/<chatname>/user/<username>/addmessage/<message>`

Esta extensión sirve para añadir un mensaje de un usuario a un chat. Solo se podrá insertar si el usuario y el chat existen en la base de datos.


url = http://localhost:5000/chat/BeforeSunrise/Celine/addmessage/Isn't everything we do in life a way to be loved a little more
res = requests.get(url)

## Obtener todos los mensajes de un chat

`/chat/<chatname>/list`

Al introducir esta extensión, devuelve un json con el nombre del chat y todos los mensajes enviados por el mismo. El chat debe existir previamente en la base de datos, si no devolverá un error.

url = http://localhost:5000/chat/BeforeSunrise/list
res = requests.get(url)

## Análisis de sentimientos

`/chat/<chatname>/sentiment`

Exta extensión devuelve un análisis de los sentimientos de los mensajes mandados por el chat. Realiza un análisis de cada mensaje y posteriormente hace una media de todos ellos para devolver un índice (entre 0 y 1) de la positividad y negatividad de los mensajes enviados por el chat.


url = http://localhost:5000/chat/BeforeSunrise/sentiment
res = requests.get(url)


### Estructura de la base de datos

Los datos en la base de datos mongo db se guardan en tres colecciones distinas: usuarios, chats, mensajes. Están interrelacionadas por el id del usuario y el id del chat que se crea automáticamente en mongodb al insertar un dato nuevo.

### Conocimientos
​
Crear una API utilizando flask
Utilizar pymongo para insertar métodos
NLTK análisis de sentimientos, mediante un módulo de python
MongoDB

​
[https://flask.palletsprojects.com/]
[https://www.getpostman.com/]
[https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.insert_one]
[https://api.mongodb.com/python/current/tutorial.html]
[https://mermaid-js.github.io/mermaid/#/entityRelationshipDiagram]​









