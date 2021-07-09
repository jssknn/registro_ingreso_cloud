# registro_ingreso_cloud
Solución que registra el ingreso de vehículos de manera autónoma a través del análisis imagenes tomadas por una cámara. 

Aplicación para que los registros puedan ser accedidos por usuarios.

## Detalles de la solución
1) Se ejecuta el script w_upload_S3.py en la máquina que va a recibir las fotos de la cámara.
    - Script w_upload_S3.py:
    Detecta la creación de un nuevo archivo en una carpeta específica, es este caso c:/fotos.
    Al producirse el evento de creación, sube el archivo a un bucket de S3.

    Este paso puede ser reemplazado por una cámara que envíe las fotos directamente al bucket de S3.

2) Creación de un bucket en S3 para recibir las fotos.
  Creación de una función en LAMBDA con el código presente en lambda.py que se invoca a partir del evento de creación de archivos en el bucket de S3.
  Creación de tabla "fotos" en DYNAMODB con los campos "fecha" y "patente" del tipo string.

    - Script lambda.py:
    Detecta el archivo creado en S3, lo envía a REKOGNITION para extraer el texto y 
    con el resultado escribe un registro fecha-hora y patente en la tabla fotos de DYNAMODB.
    
    La lectura considera al texto como una patente válida si cumple las siguientes condiciones:
      - Letras en mayúsculas.
      - Longitud mayor a 5 y menor que 10.
      - Posea exactamente 3 dígitos.
      
    Si el texto detectado no cumple estas condiciones, es informado como "No detectable".

3) Se corre el script flaskaws.py en una instancia de EC2.
    - Script flaskaws.py:
    Servicio web que obtiene los registros de la tabla fotos de DYNAMODB y los presenta en formato TABLA.

Tener en cuenta lo siguiente:
  - El costo de EC2 varía según los requerimientos que hagamos sobre la instancia (Disco, CPU, Memoria)
  y la transferencia de datos, aunque en este caso son muy altos los límites.
  - El costo de Rekognition DetectText es de u$s 1 cada 1000 consultas.
  - El costo de DynamoDB para esta solución es mínimo. Ej: Una tabla con 10000 escrituras y 1000000 lecturas cuesta u$s0,02 por mes.
  - El costo de almacenamiento y peticiones en S3 para esta solución es mínimo. 
  Ej: 5gb y 10000 peticiones al mes cuestan u$s 0,17.

Todo la implementación se puede hacer con la capa gratuita de aws.

Se agregan archivos para realizar el despliegue de la app en EC2 a través de contenedores junto con gunicorn y nginx.

## Diagrama
![alt text](https://github.com/jssknn/registro_ingreso_cloud/blob/main/diagrama.png)

## Funcionamiento
![funcionamiento](https://github.com/jssknn/registro_ingreso_cloud/blob/main/func.gif)

