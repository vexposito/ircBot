from xmlrpclib		import ServerProxy	
import os

##########################################################################################
##################################### CONEXION ###########################################
##########################################################################################

puerto 	=  8000
rpc		= ServerProxy('http://localhost:8000', allow_none=True)
# Cliente = Cliente()
print"Conectando...\n"

##########################################################################################
################################## FUNCIONES DEL CLIENTE #################################
##########################################################################################

def crear():
	print " \n Introduce los datos para crear el Bot: "
	servidor	= raw_input(" Servidor al que te quieres conectar: ")
	puerto		= input(" Puerto del servidor al que te quieres conectar: ")
	canal		= raw_input(" Canal al que te quieres conectar: ")
	canal 		= "#" + canal
	usuario		= raw_input(" Nombre de usuario: ")
	patron		= raw_input(" Patron de busqueda: ")
	patron 		= [ patron ]
	# patron 		= ['wola', 'qtal']
    # patron 		= patron.find(",")
	# patron 		= patron.replace(",", "','", 1)
	# patron 		= "['" + patron + "']"
	print "\n>> Creando Bot con los parametros introducidos..."
	rpc.crear(servidor, canal, usuario, puerto, patron)

def parar():
	ID_Bot		= raw_input("ID del BOT que quieres desconectar: ")
	parar		= rpc.desconexion(ID_Bot)
	print">> Parando Bot..."

def error():
	print ">> Error, desconectando."
	exit()

def consulta_evn():
	print ">> Consulta de eventos capturados iniciada...\n"
	rpc.consulta_DB_evn()

def consulta_msg():
	print ">> Consulta de mensajes capturados iniciada...\n"
	rpc.consulta_DB_msg()

def consulta_bot():
	print ">> Consulta de registro de BOT iniciada...\n"
	rpc.consulta_DB_bot()

def estado():
	print ">> Consulta de registro de BOT iniciada...\n"
	rpc.estado()

#def estado():


##########################################################################################
##################################### MENU DEL CLIENTE ###################################
##########################################################################################

while True:
		print "################################## "
		print "  1: Crear Bot"
		print "  2: Parar Bot"
		print "  3: Ver mensajes capturados"
		print "  4: Ver eventos capturados"
		print "  5: Ver registro de bot"
		print "  6: Estado del Bot"
		print "  7: Prueba"
		print "  8: Salir"
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
			raw_input("Has pulsado la opcion 3: MENSAJES...\npulsa una tecla para continuar\n")
			print "################################## "
			consulta_msg()

		elif opciones=="4":
			print ""
			raw_input("Has pulsado la opcion 4: EVENTOS...\npulsa una tecla para continuar\n")
			print "################################## "
			consulta_evn()

		elif opciones=="5":
			print ""
			raw_input("Has pulsado la opcion 5: BOT...\npulsa una tecla para continuar\n")
			print "################################## "
			consulta_bot()

		elif opciones=="6":
			print ""
			raw_input("Has pulsado la opcion 5: ESTADO...\npulsa una tecla para continuar\n")
			print "################################## "
			estado()

		elif opciones=="7":
			print ""
			raw_input("Has pulsado la opcion 6: PRUEBA...\npulsa una tecla para continuar\n")
			print "################################## "
			prueba()
			# rpc.prueba(msg)

		elif opciones=="8":
			break

		else:
			print ""
			raw_input("No has pulsado ninguna opcion correcta...\npulsa una tecla para continuar\n")
			print "################################## "





