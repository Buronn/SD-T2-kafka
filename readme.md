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

### 1 ¿Por qué Kafka funciona bien en este escenario?
Kafka es un software que permite el flujo y envío de información en gran volumen a través de su sistema de tópicos (brokers). Esto último permite a los servicios de Login y Bloqueo trabajar de manera asíncrona gracias al modelo productor/consumidor, dado que el servicio de Login es capaz de informar en el tópico de kafka cuales son las cuentas que han tratado de iniciar sesión de manera fallida, sin necesidad de esperar a que el servicio de bloqueo realice alguna acción, puesto que kafka se encarga de almacenar esto en el tópico el cual puede ser consumido por el servicio de Bloqueo en cualquier otro momento. 

Esto se traduce en un menor tiempo de respuesta para el usuario que esté utilizando el cliente o aplicación, ya que de no utilizar kafka la aplicación estaría esperando la respuesta del servicio de bloqueo (parecido a un modelo cliente/servidor) que en términos de escalabilidad resulta ineficiente, generando un cuello de botella que colapsaría este servicio.

### 2 Basado en las tecnologías que usted tiene a su disposición (Kafka, backend) ¿Qué haría usted para manejar una gran cantidad de usuarios al mismo tiempo?
Una opción inicial sería escalar kafka con más brokers o equipos de manera distribuida para lograr comunicar una mayor cantidad de datos en tiempo real. Adicional a esto último, también sería una buena opción distribuir el servicio de bloqueos agregando los siguientes servicios.

####
- Apache Flink: Flink es una herramienta de procesamiento de flujo en tiempo real y de código abierto, cuya funcionalidad radica en el procesamiento de múltiples tareas realizas simultáneamente en tiempo real, basado en algún tipo de input que provean datos y output donde se escribir o guardar los resultados obtenidos de estos procesamientos. Esta herramienta es ideal, puesto que nos permitiría consumir el tópico de kafka que contiene la lista de logins de usuarios, y determinar en tiempo real cuales cuentas deberán ser bloquedas.

- Redis: Es una base de datos en memoria NoSQL que se usa principalmente para la obtención de warmdata. En este servicio se almacenarían los resultados tras el procesamiento del servicio de flink, los cuales serían consumidos a través de la API del servicio de bloqueo.
####

A partir de esta arquitectura, será posible manejar una gran cantidad de usuarios en tiempo real, puesto que el servicio de bloqueo solamente accede a los datos almacenados en cache (Redis). El trabajo de procesamiento y análisis para determinar en el tiempo cuales cuentas corresponde a ser bloqueadas es llevado a cabo por Flink. Evitando lecturas y escrituras de archivos de manera ineficiente que solo empeora el rendimiento del sistema.

## ℹ Información Importante
El uso de las imágenes de [Bitnami](https://hub.docker.com/u/bitnami) fueron reemplazadas por [wurstmeister](https://hub.docker.com/u/wurstmeister) por el simple hecho de que la utilización de [AIOKafka](https://github.com/aio-libs/aiokafka) no permitía establecer una conexión con el contenedor de Kafka. Esta librería de Python permite utilizar Kafka de manera asincrónica, exactamente lo que se requería para combinar Flask con un KafkaProducer. Para el api de bloqueo se usó un KafkaProducer asíncrono basado en la contribución de trabajo de [NimzyMaina](https://github.com/NimzyMaina/flask_kafka).
