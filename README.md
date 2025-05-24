## Automarización de Pruebas para aplicacion Urban.Routes

Plataforma usada fue Urban.Routes por medio de servidor actualizado en el archivo de data.py
con este proyecto se implementaron test automatizados haciendo toda la simulacion de un usuario/a haria para pedir un taxi
en la aplicacion Urban.Routes , haciendo un recorrido por el ingreso de su ruta , tipo de tarifa, medios de pago, comentrios
al conductor, servicios adicionales y finalmente pedir el servicio 


## ARCHIVOS Y DIRECTORIOS USADOS
Creados en Github :
- data.py: se consignaron todos los cuerpos necesarios para los test como apoyo
- main.py: se encuentra todo el proyecto separado en 3 partes 
 1. class UrbanRoutesPage - se encuentran todos los localizadores 
y metodos de las pruebas con las que estan relacionados casa uno 
2.  class TestUrbanRoutes - donde están ubicadas todas las pruebas hechas segun el proyecto del sprint 8  
 
### TECNOLOGIAS USADAS
pytest : framework usado para automatizar - descargado desde Python Packages
requests: Biblioteca de Python usada para las solicitudes HTTP ( GET) - Descargado desde Python Packages en el buscador escribir pytest o desde la terminal con el comando : pip install pytest
Clonar repositorio : git@github.com:KIbanez-Tri/qa-project-Urban-Grocers-app-es.git


### Como ejecutar el proyecto
desde la terminal con el comando: pytest -v
Desde la consola con el boton de Run
Necesitas tener instalados los paquetes pytest y request para ejecutar las pruebas.