# Stori Software Engineer
En este proyecto se encuentran dos carpetas con el mismo script que cumple las funcionalidades de:  
* Estructurar un correo electrónico que contiene información sobre el saldo total de la cuenta, la cantidad de transacciones agrupadas por mes y los montos promedio de crédito y débito agrupados por mes. Usando como fuente de informacion el archivo csv.
* Guarda la transacción y la información de la cuenta en una base de datos
* Da estilo al correo electrónico e incluye el logotipo de Stori
## Docker
La carpeta docker contiene todos los archivos necesarios para realizar un despliegue en docker compose, este habilita una base de datos mysql y el script en una imagen, que al momento de correr la imagen inicia el script y se ejecuta una sola vez.
Para poder ejecutarlo primero debe correr el comando `docker-compose up -d` finalizado el proceso se puede verificar que el script corrio correctamente con: `docker-compose logs scriptrun`. En caso de no ejecutarse correctamente puede volver a probar con el siguiente comando `docker start docker_scriptrun_1`
## AWS
Esta carpeta contiene un template.yml que genera el despliegue de una lambda conectada a un api gateway para ser llamda cada que se consulta el endpoint. Este template se puede implementar desde cloudformation.
Nota: Debido a falta de cuenta en AWS no pudo ser probada