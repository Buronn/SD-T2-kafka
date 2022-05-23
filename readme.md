<br />
<div align="center">

  <h3 align="center">Sistemas Distribuidos: Tarea 02</h3>

  <p align="center">
    Fernando Burón, Felipe Condore
  </p>
</div>


## Acerca del proyecto

El objetivo de esta tarea consiste en poner en práctica el concepto de Streaming, visto en clases y presentaciones. Para ello se debe hacer uso de tecnlogías que permitan la solución a esta problemática



### 🛠 Construído con:

Esta sección muestra las tecnologías con las que fue construído el proyecto.

* [Apache Kafka](https://kafka.apache.org)
* [Postgres](https://www.postgresql.org)
* [Python](https://www.python.org)
* [Docker](https://www.docker.com)


## 🔰 Comenzando

Para iniciar el proyecto, primero hay que copiar el repositorio `git clone https://github.com/Buronn/SD-T2-kafka`, ingresar a él `/cd SD-T2-kafka` y escribir el siguiente comando en la consola:
* docker
```sh
docker-compose build
```
Para que los contenedores se inician en el ambiente local se utiliza el siguiente comando en la consola:
* docker
```sh
docker-compose up -d
```
### Pre-Requisitos

Tener Docker y Docker Compose instalado
* [Installation Guide](https://docs.docker.com/compose/install/)



## 🤝 Uso

La aplicación tiene dos API dispoble, una en el puerto 3000 (LOGIN) y otra en el 5000 (BLOCKED).

### API-LOGIN
Inicia sesión, si se hace 5 inicios incorrectos, en [API-BLOCKED](./readme.md/###API-BLOCKED)
```sh
curl --location --request POST http://localhost:3000/login \
--header 'Content-Type: application/json' \
--data-raw '{
    "user":"user",
    "pass":"password"
}'
```
#### 
- ☄ MÉTODO: POST
- ❔   CONTENT-TYPE: application/json
- 📄  DATA-RAW: user y password en formato json

#### Response example
```js
// En caso de colocar una contraseña incorrecta
{
    "error":"Wrong password"
}
// En caso de colocar correctamente los datos
{
    "success":True
}
```
En caso de que se deba registrar un usuario, utilizar la siguiente petición:
```sh
curl --location --request POST 'localhost:3000/register' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user":"test",
    "pass":"test1234"
}'
```
### API-BLOCKED
Muestra los usuarios bloqueados por muchos intentos fallidos
```sh
curl −−location −−request GET http://localhost:5000/blocked
```
#### 
- ☄ MÉTODO: GET
#### Response
```js
{
    "users-blocked":[
      "user1",
      "user2"
    ]
}
```
## ❔ Preguntas

####
### 1 ¿Por qué Kafka funciona bien en este escenario?
#### Debido a que
### 2 Basado en las tecnologías que usted tiene a su disposición (Kafka, backend) ¿Qué haría usted para manejar una gran cantidad de usuarios al mismo tiempo?
####

## ℹ Información Importante
El uso de las imágenes de [Bitnami](https://hub.docker.com/u/bitnami) fueron reemplazadas por [wurstmeister](https://hub.docker.com/u/wurstmeister) por el simple hecho de que la utilización de [AIOKafka](https://github.com/aio-libs/aiokafka) no permitía establecer una conexión con el contenedor de Kafka. Esta librería de Python permite utilizar Kafka de manera asincrónica, exactamente lo que se requería para combinar Flask con un KafkaProducer.
