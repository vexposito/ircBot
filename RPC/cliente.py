from xmlrpclib		import ServerProxy	#	CLIENTE:
import os

##########################################################################################
##################################### CONEXION ###########################################
##########################################################################################
puerto 	=  8000
rpc		= ServerProxy('http://localhost:8000',allow_none=True)
# Cliente = Cliente()
print"Conectando...\n"

##########################################################################################
################################## FUNCIONES DEL CLIENTE #################################
##########################################################################################

# class Cliente():
# 	def __init__(self):

def crear():
	# servidor		= "irc.irc-hispano.org"
	# puerto		= 6667
	# canal			= "#ircVero"
	# usuario		= "ircVeroVerox"
	# patron		= "hola"
	# print "\n>> Creando Bot con los parametros introducidos..."

	print " \nIntroduce los datos para crear el Bot: "
	servidor	= raw_input("Servidor al que te quieres conectar: ")
	puerto		= input("Puerto del servidor al que te quieres conectar: ")
	canal		= raw_input("Canal al que te quieres conectar: ")
	canal 		= "#" + canal
	usuario		= raw_input("Nombre de usuario: ")
	patron		= raw_input("Patron de busqueda: ")
    # patron 		= patron.find(",")
	# patron 		= patron.replace(",", "','", 1)
	# patron 		= "['" + patron + "']"
	print "\n>> Creando Bot con los parametros introducidos..."
	# print ">> Conectando al servidor... \n" #+ servidor + " \nEn el puerto: " + puerto + " \nCon el usuario: " + usuario + " \nNuestro patron de busaqueda sera: " + patron + "\n"
	
	rpc.crear(servidor, canal, usuario, puerto, patron)

def parar(servidor, canal, usuario, puerto, patron):
	cliente		= ServerProxy('http://localhost:8000', allow_none=True)
	parar		= rpc.desconexion(servidor, canal, usuario, puerto, patron)
	print">> Parando Bot..."

def mensajes(servidor,canal,usuario,puerto,patron):
	cliente		= ServerProxy('http://localhost:8000', allow_none=True)
	mensajes	= rpc.mensaje(servidor, canal, usuario, puerto, patron)
	print ">> Peticion de visualizacion de los mensajes capturados..."

def eventos(servidor,canal,usuario,puerto,patron):
	cliente		= ServerProxy('http://localhost:8000',allow_none=True)
	eventos		= rpc.eventos(servidor, canal, usuario, puerto, patron)
	print ">> Peticion de visualizacion de los eventos capturados..."

def error():
	print ">> Error, desconectando."
	exit()

def prueba():
	print "Bienvenido a PRUEBA\n"
	msg	= raw_input("Introduce un mensaje: \n")
	rpc.prueba(msg)
	

# crear()
# Parametros de ejemplo/prueba:
# servidor: irc.irc-hispano.org
# puerto:6667
# canal: ircVero
# nombre:ircVero3434
# patron: hola


#defestado():


##########################################################################################
##################################### MENU DEL CLIENTE ###################################
##########################################################################################

while True:
		print "################################## "
		print "  1: Crear Bot"
		print "  2: Parar Bot"
		print "  3: Ver mensajes capturados"
		print "  4: Ver eventos capturados"
		print "  5: Estado del Bot"
		print "  6: Prueba"
		print "  7: Salir"
		print "################################## "
		 # solicituamos una opcion al usuario
		opciones = raw_input("  Inserta un numero valor >> ")
		print "################################## "
	 	
		if opciones=="1":
			print ""
			raw_input("Has pulsado la opcion 1: CREAR...\npulsa una tecla para continuar")
			print "################################## "
			crear()
			

		elif opciones=="2":
			print ""
			raw_input("Has pulsado la opcion 2: PARAR...\npulsa una tecla para continuar\n")
			parar()

		elif opciones=="3":
			print ""
			raw_input("Has pulsado la opcion 3: EVENTOS...\npulsa una tecla para continuar\n")
			eventos()

		elif opciones=="4":
			print ""
			raw_input("Has pulsado la opcion 4: MENSAJES...\npulsa una tecla para continuar\n")
			mensajes()

		elif opciones=="5":
			print ""
			raw_input("Has pulsado la opcion 5: ESTADO...\npulsa una tecla para continuar\n")
			estado()

		elif opciones=="6":
			print ""
			raw_input("Has pulsado la opcion 6: PRUEBA...\npulsa una tecla para continuar\n")
			prueba()
			# rpc.prueba(msg)

		elif opciones=="7":
			break

		else:
			print ""
			raw_input("No has pulsado ninguna opcion correcta...\npulsa una tecla para continuar\n")





