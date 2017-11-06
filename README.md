# ClienteSMB
Cliente SMB en python para AS400
Para que un AS400 puede utilizar recursos remotos (carpetas compartidas) mediante el protocolo CIFS a samba es necesatio configurar varios aspectos del AS400.

Para usar el cliente smb que trae por defecto iSeries es necesario poder configurar varios aspectos:
	Es necesario crear una carpeta con el nombre o la dirección Ip del nombre del servidor al que queramos acceder, dentro de la carpeta QNTC del sistema de ficheros del iSeries. 
	Esta carpeta se borra automáticamente cada vez que se reinicia el iSeries. Es decir hay que automatizar la creación de la carpeta en cada reinicio de la máquina iSeries.
	Además es necesario que el usuario que acceda al aceda al recurso compartido remoto esté definido en el servidor remoto.
	Estas dos limitaciones son muy importantes y demasiado exigentes, a veces no es posible sincronizar los usuarios entre ambos sistemas, el iSeries y el servidor Remoto.
	Además esto es un riesgo de seguridad pues el mismo usuario y contraseña que accede al recurso remoto debe existir en el iSeries.
	Otra limitación que se trata de subsanar es que al estar integrados los usuarios entre las distintas máquinas, todos los usuarios del iSeries que quieran acceder al recurso remoto deben estar en elos dos sistemas.
	
Con el cliente escrito en python se trata de mitigar estos riesgos de seguridad. 
El sistema remoto crea uno o varios usuarios para el acceso a estas carpetas remotas y con este usuario los usuarios de AS440 podrán acceder a dejar ficheros o a subirlos a nuestro AS400.

Para poder usar esto es necesario instalar en el AS400 python. Hay dos posibilidades instalar desde los CD originales que IBM proporciona (para versiones 7 de OS400) o instalar python 2.7 desde la web http://www.iseriespython.com/
Las pruebas está hechas con la versión de este último port.

