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

Para iniciar el proyecto, primero hay que copiar el repositorio y luego escribir el siguiente comando en la consola:
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

La aplicación tiene una API, que a través del método GET se pueden hacer las siguientes consultas:

### Query
Busca el inventario según la coincidencia de la palabra otorgada, busca en Cache y luego en la Base de Datos.
```curl
curl −−location −−request GET http://localhost:3000/inventory/search?q=Disk
```
#### 
- ☄METODO: GET
- 🔑KEY: q
- 📃VALUE: \<palabra a buscar\>

#### Response example
```js
{
    "items": [
        {
            "id": 10,
            "name": "SanDisk SSD PLUS 1TB Internal SSD - SATA III 6 Gb/s",
            "price": 109,
            "category": "electronics",
            "count": 470
        }
    ]
}
```
### Reset
Borra el cache de Redis.
```curl
curl −−location −−request GET http://localhost:3000/reset
```
#### Response
```sh
Cache flushed
```

### Keys
Muestra las Keys que ha guardado el cache.
```curl
curl −−location −−request GET http://localhost:3000/keys
```
#### Response
```js
[
    "SSD",
    "Slim",
    "Mens",
    "Disk",
    "6"
]
```
## Comparación algoritmos de remoción
Para llevar a cabo una comparación entre los algoritmos se preparó un bash script que se puede correr desde cualquier contenedor o ambiente de linux. El archivo corresponde a request.sh, y realiza una serie de peticiones http a través del comando curl, donde el output corresponde a la palabra que se busca en la API Rest y el tiempo en milisegundos que se demora en realizar la petición.
```sh
bash requests.sh
```
Cabe destacar que para comparar los distintos algoritmos es necesario cambiar la política de remoción del contenedor de redis. Para ello basta cambiar la variable de entorno maxmemorypolicy entre `allkeys-lru` y `allkeys-lfu` que se encuentra en el archivo .env, e ir aplicando los cambios usando `docker-compose up -d` cada vez que se ejecutará el bash script.
### Características
| LFU | LRU |
| ------------- | ------------- |
| Remueve el ítem menos utilizado. | Remuevo el ítem que menos se ha usado reciéntemente. |
| Debe mantener una cola para registrar todos los registros de acceso a datos, y cada información debe mantener un recuento de referencia. | Por cada hit dado en cache se deben buscar el dato pedido y actualizar el encabezado. |
| Prioriza la ítems más accedidos a largo plazo. | Prioriza los ítems más recientes en el caché. |

### Mediciones
#### Sin cache
| Palabra | LFU | LRU |
| ------------- | ------------- | ------------- |
| Disk | 7.922000 ms | 7.295000 ms |
| SSD | 6.721000 ms | 6.751000 ms |
| SATA | 6.792000 ms | 7.398000 ms |
| Mens | 7.133000 ms | 7.346000 ms |
| a | 7.206000 ms | 7.283000 ms |

#### Con cache
| Palabra | LFU | LRU |
| ------------- | ------------- | ------------- |
| Disk | 2.413000 ms | 2.251000 ms |
| SSD | 2.234000 ms | 2.940000 ms |
| SATA | 3.149000 ms | 2.091000 ms |
| Mens | 2.131000 ms | 2.188000 ms |
| a | 3.182000 ms | 2.749000 ms |
