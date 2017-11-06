#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

def CrearSiExiste(carpeta):
	# creamos la carpeta o carpetas de una ruta si no existe
	# Devolvemos True si la hemos creado y False si no hemos hecho nada
	import os
	Aux = False
	if not os.path.exists(carpeta):
		os.makedirs(carpeta)
		Aux = True
	return Aux

def comprimir(archivo, destino, nombrecomprimido='Nombre'):
	# Comprimimos en formato zip el fichero: archivo 
	# en el archivo zip: destino
	# Para que el fichero zip generado no guarde la ruta local generada del AS400
	# utilizaremos el nombre de fichero: nombrecomprimido
	# nombrecomprimido es el nombre zip que queramos que lo vea
	# el usuario que reciba el fichero zip
	
	# archivo y destino deben tener la ruta completa 
	# para que se vea y lo puedan ejecutar
	import zipfile
	import os
	Aux = False
	# Creamos la carpeta destino por si no lo hubiera
	carpeta = os.path.dirname(destino)
	CrearSiExiste(carpeta)
	try:
		import zlib
		compression = zipfile.ZIP_DEFLATED
	except:
		compression = zipfile.ZIP_STORED
	if (os.path.isfile(archivo)):
		zf = zipfile.ZipFile(destino, mode="w")
		try:
			zf.write(archivo, nombrecomprimido, compress_type=compression)
			Aux = True
			#zf.write(archivo, compress_type=compression)
		finally:
			zf.close()
	return Aux