# -*- coding: UTF-8 -*-
# Librerias de PaqueteSBM.
from PaqueteSBM.ficheros import comprimir
from PaqueteSBM.ficheros import CrearSiExiste
from PaqueteSBM.ClienteSMB import getBIOSName
from PaqueteSBM.ClienteSMB import ListaRecursosServidor
from PaqueteSBM.ClienteSMB import SubirFichero
from PaqueteSBM.ClienteSMB import Descargar
import socket

# ir comentado lo que no se quiera ejecutar

# Averiguo la Ip del AS400 y su nombre
iplocal = socket.gethostbyname(socket.gethostname())
print getBIOSName(iplocal) + '(' + iplocal + ')'


# Variables de acceso
userID = 'USER' # Usuario del sistema remoto a acceder
password= 'PASS' # Password del sistema remoto a acceder
remote_smb_ip = '192.168.1.11' # Direccion Ip del servidor remoto
domain_name = 'DOMINIO' # Dominio del servidor Windows o remoto
local_ip = '127.0.0.1' # Dirección Ip de la máquina local, no es necesario, ver las líneas de más arriba

# Obtengo los nombre de las máquinas remotas
server_ip = getBIOSName(remote_smb_ip, timeout=5)
print remote_smb_ip + '(' + server_ip + ')'
client_machine_name = getBIOSName(local_ip, timeout=5)
print client_machine_name + '(' + local_ip + ')'

# Obtengo la lsiata de los recursos remotos
print ListaRecursosServidor(userID, password, local_ip, remote_smb_ip, domain_name)

# Variables del fichero
Nombre_Recurso = 'Datos' # Nombre del recurso remoto, es posible obtenerlo de la función ListaRecursosServidor
path_destino = '/Papelera/' # Ruta del servidor remoto
filename = '/Docs/fichero.pdf' # Nombre del fichero del IFS que queramos subir al servidor remoto

# Subimos el fichero, filename debe existir
SubirFichero(userID, password, local_ip, server_ip, domain_name, Nombre_Recurso, path_destino, filename)

# Hacemos otra prueba
Nombre_Recurso = 'Datos'
path_destino = '/Papelera/'
filename = '/Docs/novale.TXT' # Este fichero debe exstir en el iSeries
SubirFichero(userID, password, local_ip, server_ip, domain_name, Nombre_Recurso, path_destino, filename)

#Prueba a generar un fichero zip
comprimir(filename, '/Docs/novale.zip', 'kk.txt')
SubirFichero(userID, password, local_ip, server_ip, domain_name, Nombre_Recurso, path_destino, '/Docs/asociados.zip')

# Descargar se tiene que verificar para que funcione con ficheros binarios, no solo texto
Nombre_Recurso = 'Datos' # Nombre de recurso remoto
path_destino = '/Papelera/' # Ruta donde se encuentra el archivo
filenameremoto = '1.jpg' # Nombre del fichero (debe existir)
NombreFicheroIFS = '/Docs/novale.jpg' # Nombre completo donde dejará el fichero en el IFS
Descargar(userID, password, local_ip, server_ip, domain_name, Nombre_Recurso, path_destino, filenameremoto, NombreFicheroIFS)


