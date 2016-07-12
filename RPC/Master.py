import threading
import xmlrpclib
import sqlite3
import time
from Bot import Bot
from SimpleXMLRPCServer import SimpleXMLRPCServer	#		SeimportaelmoduloXMLRPC
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


##########################################################################################
####################################### HEBRAS ###########################################
##########################################################################################

class HebraBot(threading.Thread):
    def __init__(self, servidor, canal, nombre, puerto, patron, ID_Bot):
        # Esto hay que hacerlo siempre: 
        threading.Thread.__init__(self)    

        # Copiamos como atributos los parametros:
        self.servidor     = servidor
        self.canal        = canal
        self.nombre       = nombre
        self.puerto       = puerto
        self.patron       = patron
        self.ID_Bot       = ID_Bot
        #Conexion BD
        print "Abriendo BD..."
        self.con        = sqlite3.connect('irc.db')  #con_bd.close()
        self.cursor     = self.con.cursor()  #cursor.close()

        #Generamos un ID para el BOT y registramos el BOT:
        print "Registrar BOT"
        self.registro_Bot(self.servidor, self.canal)

        # Creamos el objeto "bot":
        self.bot    = Bot(self.servidor, self.canal, self.nombre, self.puerto, self.patron, self.ID_Bot, self.ID_convers);

    # Lo que tiene que hacer en concurrencia:
    def run(self):
        print ">> lanzando bot... " 
        return self.bot.conexion()

    def existe_ID(self, ID_Bot):
        # print "  >>>> Probando si ID '" + self.ID_Bot + "' existe..."
        self.cursor.execute("SELECT ID_Bot FROM BOT_INFO WHERE ID_Bot == '" + str(self.ID_Bot) + "'")            
        if (self.cursor.fetchone()) != None:
              return True
        else:
              return False

    def generar_ID_Bot(self):
        probarDeNuevo   = True
        numerito        = 0
        while probarDeNuevo:   
            numerito = numerito + 1         
            # numerito          = random.choice(range(100))
            self.ID_Bot       = 'BOT' + str(numerito)
            # print "\n  >> Probando ID: " + self.ID
            if self.existe_ID(self.ID_Bot) == False:
                probarDeNuevo = False
                print "  >> ID... OK"
                print "  >> El ID del BOT es: " + self.ID_Bot + "\n  >> Anota el ID para futuras modificaciones.\n"
            else: 
                probarDeNuevo = True 
                # print "  >> El ID ya existe, probando otro..."        

        threading.Thread(name = self.ID_Bot)   
        return self.ID_Bot

    def registro_Bot(self, servidor, canal):
        tiempo_ini      = time.strftime('%d %b %y / %H:%M:%S')
        t1              = time.strftime('%H %M %S')
        self.ID_convers      = t1.replace(" ", "")
        tiempo_fin      = 0
        eventos         = 0
        estado          = "ON"
        num_msg         = 0
        print " Generando ID..."
        self.ID_Bot  = self.generar_ID_Bot()  
        print " Registrando " + self.ID_Bot
        self.cursor.execute(
            "INSERT INTO BOT_INFO (ID_CONVERS, ID_BOT, INICIO, ULTIMA, SERVIDOR, CANAL, EVENTOS, NUM_MSG, ESTADO) VALUES ('"
            + str(self.ID_convers) +"','"+ str(self.ID_Bot)+"','"+ str(tiempo_ini) +"', '"+ str(tiempo_fin) +"',' "
            + str(self.servidor) +"', '"+ str(self.canal) +"', '"+ str(eventos) + "', '"
            + str(num_msg) + "', '"+ str(estado) +"')"
            )
        self.con.commit() 
        self.cursor.fetchone()
        print " Ok!  Registrado correctamente.";
        self.con.close()
        reintentar = False

    def desconexion(ID_Bot):
        print " Desconectando..."
        Bot.desconexion(self.ID_Bot)

    def estado(ID_BOT):
        threading.isAlive(name = ID_BOT)
        threading.enumerate()


##########################################################################################
################################## FUNCIONES SERVIDOR ####################################
##########################################################################################

def crear(servidor, canal, nombre, puerto, patron):
    print "Creando Hebra..."
    ID_Bot = 0
    hebra	= HebraBot(servidor, canal, nombre, puerto, patron, ID_Bot)
    # HebraBot.run(servidor,canal,nombre,puerto,patron)
    hebra.start()

def desconexion(ID_Bot):	
    print "Desconectando Bot con ID:" +  ID_Bot
    HebraBot.desconexion(ID_Bot)	

def conectar_DB():
    con = None
    try:         
        con        = sqlite3.connect('C:/DjangoProyectos/irc.db')  #con_bd.close()
        cursor     = con.cursor()  #cursor.close()
        reintentar = False
        print " OK!  DB Abierta."
    except:
        print " ERROR! Reintentando conexion con la DB."
    return con


def cerrar_DB():
    print "Cerrando DB..."
    cursor.close()
    con.close()

def consulta_DB_msg():
    conectar_DB()
    print u"La base de datos se abrio correctamente."
    print " ## TABLA DE MENSAJES ##"
    cursor.execute("SELECT ID_MSG, FECHA, CANAL, SERVIDOR, USUARIO, MENSAJE FROM MENSAJES")
    for i in cursor:
        # print "ID     |    FECHA   |   CANAL   |   SERVIDOR   |   USUARIO   |    MENSAJE"
        # print i[0] +" | "+ i[1] +" | "+ i[2] +" | "+ i[3] +" | "+ i[4] +" | "+ i[5] 
        print "ID_MSG   = ", i[0]
        print "FECHA    = ", i[1]
        print "------------------------------------------------"
        print "   CANAL   |       SERVIDOR       |   USUARIO"
        print "------------------------------------------------"
        print i[2] + "   | " + i[3] + "  | " + i[4]
        print "------------------------------------------------"
        # print "FECHA    = ", i[1]
        # print "CANAL    = ", i[2]
        # print "SERVIDOR = ", i[3]
        # print "USUARIO  = ", i[4]
        print "MENSAJE  = ", i[5], "\n"
        print "################################################", "\n"

    print "Operacion realizada con exito."
    cerrar_DB()

##--------------------------------------------------------------------------------------------------------------------------##
def consulta_DB_evn():
    # conectar_DB()
    print u"La base de datos se abrio correctamente."
    print " ## TABLA DE EVENTOS ##"
    cursor.execute("SELECT ID_EVENT, FECHA, CANAL, SERVIDOR, PATRON FROM EVENTO")
    for i in cursor:
        print " ID_EVENT = ", i[0]
        print " FECHA    = ", i[1]
        print " CANAL    = ", i[2]
        print " SERVIDOR = ", i[3]
        print " PATRON   = ", i[4], "\n"
        print "#####################################", "\n"

    print "Operacion realizada con exito."
    # cerrar_DB()

##--------------------------------------------------------------------------------------------------------------------------##
def consulta_DB_bot():
    # conectar_DB()
    print " ## TABLA DE REGISTRO BOT ##"
    cursor.execute("SELECT ID_CONVERS, ID_BOT, INICIO, ULTIMA, SERVIDOR, CANAL, EVENTOS, NUM_MSG, ESTADO FROM BOT_INFO")
    for i in cursor:
        print " ID_CONVERS  = ", i[0]
        print " ID_BOT      = ", i[1]
        print " INICIO      = ", i[2]
        print " ULTIMA      = ", i[3]
        print " SERVIDOR    = ", i[4]
        print " CANAL       = ", i[5]
        print " EVENTOS     = ", i[6]
        print " NUM_MSG     = ", i[7]
        print " ESTADO      = ", i[8], "\n"
        print "#####################################", "\n"
    # cerrar_DB()

def estado(ID_Bot):      
    print "Estado BOT"
    # threading.enumerate(HebraBot)
    # threading.isAlive(ID_Bot)
    #threading.activeCount(name = ID_Bot)
    estado = HebraBot.estado(ID_Bot)
    print " Consultando estado del Bot: " + ID_Bot
    return



#########################################################################################
#################################### CONEXION ###########################################
#########################################################################################

try:

    # Lanzamos el servidor, para que escuche peticiones RPC:    
    puerto  	= 9000

    class RequestHandler(SimpleXMLRPCRequestHandler): 
        rpc_paths = ()

    # servidorRpc  =  xmlrpclib.ServerProxy ( 'http: // localhost:8000' ,  allow_none = False) 
    servidorRpc = SimpleXMLRPCServer(("localhost", puerto), logRequests = True ,  allow_none = True, requestHandler = RequestHandler) 
    print ">> Escuchando en puerto ", puerto

    # Le decimos que funciones se pueden invocar, y con que nombre:
    servidorRpc.register_function(crear, "crear")
    servidorRpc.register_function(desconexion, "desconexion")
    servidorRpc.register_function(consulta_DB_msg, "consulta_DB_msg")
    servidorRpc.register_function(consulta_DB_evn, "consulta_DB_evn")
    servidorRpc.register_function(consulta_DB_bot, "consulta_DB_bot")

    # Conectar Base de datos
    con        = sqlite3.connect('irc.db')  #con_bd.close()
    cursor     = con.cursor()  #cursor.close()

    # Dejamos que se quede escuchando el servidor RPC:
    servidorRpc.serve_forever()
             
except:
    print '>> Error en la conexion' +  exit()


