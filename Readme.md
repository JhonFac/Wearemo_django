# Backend Test Wearemo Django

Se realizan los servicios dockerizados basados en modelos y requerimientos propuestos

* Servicio Crud para  **Customer**, con la consulta de vanalnces.
* Servicio Crud para  **Loan**, con la opcion de activar o rechazar los prestamos.
* Servicio Crud para  **Pyment**, el cual crea y distribuye los detalles del pago el el servicio **PymentDetails**
* Servicio Crud para  **PymentDetails**

* **Se crea una imagen de base de datos de Postgress en Docker, la cual el mismo proyecto se conecta en produccion para tener la persistencia de datos** al igual si el contenedor esta arriba se puede conectar desde **Desarrollo**, ejecutando el proyecto en local. 

* Tambien se puede cambiar la conexión a la base de datos db.sqllite3 el cual contiene los mismos datos

## Technical requirements
The frameworks were used:

- Python 3.10^
- Django Rest-Framework
- Docker

## Build Container and image in Docker 
docker-compose build

## Run image in Docker 
docker-compose up

## RUN PROJECT ONLY IN PYTHON

Before to start, you need to install the dependencies:
`pip install -r requirements.txt`

Next, you need to create the database:
`python manage.py makemigrations`
`python manage.py migrate`

Finally, you need to create the superuser (optional):
`python manage.py createsuperuser`

To have a local env without docker it is recommended to use the following commands:

- `python3 -m venv .env`
- `. .env-mts/bin/activate`
- `pip install -r requirements.txt`

To run Project:
`python manage.py runserver`


To be able to see the documentation in swagger in the url:
`http://127.0.0.1:8000/swagger/`


## Command to run unit tests

`python manage.py test`
