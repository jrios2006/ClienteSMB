# ClienteSMB
Cliente SMB en python para AS400.

Para que un AS400 puede utilizar recursos remotos (carpetas compartidas) mediante el protocolo CIFS a samba es necesatio configurar el AS400.

## Restricciones del cliente SMB del iSeries

Para usar el cliente smb que trae por defecto iSeries es necesario poder configurar varios aspectos:
* Es necesario **crear una carpeta** con el nombre o la dirección Ip del nombre del servidor al que queramos acceder, **dentro de** la carpeta **QNTC** del sistema de ficheros del iSeries.
* **Esta carpeta se borra automáticamente cada vez que se reinicia el iSeries.**
* Es decir hay que automatizar la creación de la carpeta en cada reinicio de la máquina iSeries.
* Además es necesario que **el usuario del iSeries que acceda** al recurso compartido remoto **esté definido en el servidor remoto.**


Estas dos limitaciones son muy importantes y demasiado exigentes, a veces no es posible sincronizar los usuarios entre ambos sistemas, el iSeries y el servidor Remoto.
Además esto es un riesgo de seguridad pues el mismo usuario y contraseña que accede al recurso remoto debe existir en el iSeries.


Otra limitación que se trata de subsanar es que al estar integrados los usuarios entre las distintas máquinas, todos los usuarios del iSeries que quieran acceder al recurso remoto deben estar en elos dos sistemas.
	
Con el cliente escrito en python se trata de mitigar estos riesgos de seguridad. 


El sistema remoto crea uno o varios usuarios para el acceso a estas carpetas remotas y con este usuario los usuarios de AS440 podrán acceder a dejar ficheros o a subirlos a nuestro AS400.

Así no se publicarán usuarios del iSeries en el sistema remoto.

## Instalación de python en iSeries

Para poder usar esto es necesario instalar en el AS400 python. 

Hay dos posibilidades:

1. Instalar desde los [CD originales que IBM proporciona para versiones 7 de OS400](https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/IBM%20i%20Technology%20Updates/page/Python)

2. Instalar python 2.7 desde la web [iSeriesPython](http://www.iseriespython.com/)
Aquí no se tratar de enseñar a instalar python en el iSeries
Las pruebas están realizadas con python 2.7, iSeriesPython.

## Instalación de las librerías
Para instalar los módulos necesarios para poder usar el cliente SMB en python, es necesario descargar las carpetas:

* smb
* pyasn1
* nmb

Estas carpetas hay que colocarlas en la carpeta IFS **/python27/site-packages**, para luego poder usarlas

Para las pruebas se ha creado una carpeta con las funciones básicas para poder acceder a descargar un archivo, subir un archivo, etc.
Esta carpeta se llama **PaqueteSMB**, esta carpeta también debe ir a la ruta del IFS /python27/site-packages

## PaqueteSMB
Este fichero contiene varias funciones.

* getBIOSName - Devuelvo el nombre NetBios de una máquina remota
* ListaRecursosServidor - Devuelvo una lista con los recursos disponibles del servidor remoto
* SubirFichero - Subo un fichero del IFS (filename) al sistema de ficheros remoto
* Descargar - Descargo un fichero remoto al IFS local del AS400
* ... por definir más

## Ejemplo de uso
El ejemplo está en el fichero ejemplo.py 

Se debe modificar para introducir los parámetros necesarios para poder acceder al servidor remoto, que son:
* Usuario del servidor remoto
* Contraseña del servidor remoto
* Ip del servidor remoto
* Dominio del servidor remoto
* Recursos compartido
* Nombre de la ruta o carpeta del servidor remoto dond ese encuentran los archivos
* Nombre del fichero a subir o descargar
