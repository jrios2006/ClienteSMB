# -*- coding: UTF-8 -*-
import sys
import smb
from smb.SMBConnection import SMBConnection
from smb import smb_structs

def getBIOSName(remote_smb_ip, timeout=5):
	# Devuelvo el nombre NetBios de una máquina remota
	from nmb.NetBIOS import NetBIOS
	Aux = 'ERROR'
	try:
		bios = NetBIOS()
		srv_name = bios.queryIPForName(remote_smb_ip, timeout=timeout)
		Aux = srv_name[0]
	except:
		print 'No es posible conocer el nombre NETBIOS del servidor ' + remote_smb_ip + ' en el tiempo ' + str(timeout)
	finally:
		bios.close()
	return Aux

def ListaRecursosServidor(userID, password, local_ip, server_ip, domain_name):
	# Devuelvo una lista en formato UTF-8 con los recursos disponibles via samba
	# del servidor especificado con server_ip, con el nombre del dominio en domain_name
	# y como autenticación el usuario userID y la contraseña password
	# Si no conseguimos autenticarnos con el sistema remoto imprimos el error y damos una lista vacia
	server_name = getBIOSName(server_ip, timeout=5)
	client_machine_name = getBIOSName(local_ip, timeout=5)
	#print domain_name
	Aux = []
	if (server_name == 'ERROR'):
		print 'No somos capaces de saber el nombre remoto por NETBIOS usamos su direccion Ip: ' + server_ip
		server_name = server_ip
	try:
		#print userID, password, client_machine_name, server_name, domain_name
		conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,is_direct_tcp=True)
		conn.connect(server_ip, 445)		
		shares = conn.listShares()
		for share in shares:
			if not share.isSpecial and share.name not in ['NETLOGON', 'SYSVOL','REPL$']:
				Aux.append(share.name)
		conn.close()
	except:
		print 'Error con el usuario: ' + userID + ' y la maquina: ' + server_ip	
	return Aux

def SubirFichero(userID, password, local_ip, server_ip, domain_name, Nombre_Recurso, path_destino, filename):
	# Subo un fichero del IFS (filename) al sistema de ficheros remoto
	# Servidor, Nombre_Recurso, path_destino, filename
	import os
	Aux = False
	server_name = getBIOSName(server_ip, timeout=5)
	client_machine_name = getBIOSName(local_ip, timeout=5)
	print server_name + '/' + client_machine_name
	if (server_name == 'ERROR'):
		print 'No somos capaces de saber el nombre remoto(' + server_ip + ') por NETBIOS usamos su direccion Ip: ' + server_ip
		server_name = server_ip
	try:
		conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,is_direct_tcp=True)
	except:
		print 'Error al conectar. No podemos subir con el usuario: ' + userID + ' a la maquina: ' + server_ip + ' el fichero ' + filename
	if conn:
		conn.connect(server_ip, 445)
		print '************************'
		try:
			print 'Subimos en ' + Nombre_Recurso + path_destino + ' el fichero ' + filename
			print 'Size = %.1f kB' % (os.path.getsize(filename) / 1024.0)
			print 'start upload'
			with open(filename, 'rb') as file_obj:
				print file_obj.name
				print os.path.basename(file_obj.name)
				print os.path.dirname(file_obj.name)
				print '***************************'
				print path_destino+os.path.basename(file_obj.name)
				filesize = conn.storeFile(Nombre_Recurso, path_destino+os.path.basename(file_obj.name), file_obj, timeout=100)
			print 'upload finished'
			Aux = True
		except:
			print 'No existe el fichero ' + filename
		conn.close()		
	return Aux

def Descargar(userID, password, local_ip, server_ip, domain_name, Nombre_Recurso, path_destino, filename, NombreFicheroIFS):
	# Descargo un fichero remoto al IFS local del AS400
	# NombreFicheroIFS es el nombre con la ruta completa donde guardamos el fichero
	# Hay un problema con la codificacion de los ficheros
	# 426-Unable to convert data from CCSID 1208 to CCSID 819: reason 3021 al intentar descar por FTP el fichero y 
	# comprobar la función
	import tempfile, shutil, os
	Aux = False
	server_name = getBIOSName(server_ip, timeout=5)
	client_machine_name = getBIOSName(local_ip, timeout=5)
	print server_name + '/' + client_machine_name
	if (server_name == 'ERROR'):
		print 'No somos capaces de saber el nombre remoto(' + server_ip + ') por NETBIOS usamos su direccion Ip: ' + server_ip
		server_name = server_ip
	try:
		conn = SMBConnection(userID, password, client_machine_name, server_name, domain=domain_name, use_ntlm_v2=True,is_direct_tcp=True)
	except:
		print 'Error al conectar. No podemos acceder con el usuario: ' + userID + ' a la maquina: ' + server_ip + ' y conbseguir el fichero ' + filename
	if conn:
		conn.connect(server_ip, 445)
		file_obj = tempfile.NamedTemporaryFile()
		print("Fichero temporal: {}".format(file_obj.name))
		print type(file_obj)
		NombreFicheroTemporal = file_obj.name
		try:
			file_attributes, filesize = conn.retrieveFile(Nombre_Recurso, path_destino + filename , file_obj)
			#print file_attributes
			#print filesize
			print 'Copiamos a disco el fichero ' + path_destino + filename + ' obtenido con el nombre ' + NombreFicheroIFS
			shutil.copy(NombreFicheroTemporal, NombreFicheroIFS)
			Aux = True
		except:
			print 'No existe el fichero ' + path_destino + filename + ' en la maquina remota ' + server_name
		file_obj.close()		
		conn.close()		
	return Aux