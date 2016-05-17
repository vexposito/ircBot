import threading
import xmlrpclib
from Bot import Bot
from SimpleXMLRPCServer import SimpleXMLRPCServer	#		SeimportaelmoduloXMLRPC
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler


##########################################################################################
####################################### HEBRAS ###########################################
##########################################################################################
class HebraBot(threading.Thread):
    def __init__(self, servidor,canal,nombre,puerto,patron):
        # Esto hay que hacerlo siempre:
        threading.Thread.__init__(self)
        # Copiamos como atributos los parametros:
        self.servidor     = servidor
        self.canal        = canal
        self.nombre       = nombre
        self.puerto       = puerto
        self.patron       = patron
        # self.parar        = 0
        # veces             = 0

        # Creamos el objeto "bot":
        self.bot    = Bot(self.servidor, self.canal, self.nombre, self.puerto, self.patron);


    # Lo que tiene que hacer en concurrencia:
    def run(self):
        # while not self.parar:
        print ">> lanzando bot... " #, self.bot.conexion()," -> ", self.veces
        # print ">> parametros del bot: " + self.servidor + " " + self.canal + " " + self.nombre + " " + self.puerto + " " + self.patron
        # self.bot    = Bot(servidor,canal,nombre,puerto,patron);
        
        # self.veces = self.veces + 3
        # time.sleep(2);
        return self.bot.conexion()
    
    # def obtener_estado(self):
    #     return self.veces

##########################################################################################
################################## FUNCIONES SERVIDOR ####################################
##########################################################################################

def crear(servidor, canal, nombre, puerto, patron):
	hebra	= HebraBot(servidor,canal,nombre,puerto,patron)
	# HebraBot.run(servidor,canal,nombre,puerto,patron)
	hebra.start()

def desconexion(BOT_ID):	
	self.bot.desconexion(BOT_ID)
	print "Desconecatndo"

def prueba(msg):	
	print "has llegado " + msg
	return msg

#defestado():
#defmensajes():
#defeventos():

##########################################################################################
##################################### CONEXION ###########################################
##########################################################################################
# Lanzamos el servidor, para que escuche peticiones RPC:    
puerto  	= 8000;
class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ()

# servidorRpc  =  xmlrpclib.ServerProxy ( 'http: // localhost:8000' ,  allow_none = False) 
servidorRpc = SimpleXMLRPCServer(("localhost", puerto), logRequests = True ,  allow_none = True, requestHandler = RequestHandler) 
print "Escuchando en puerto ", puerto

# Inicializo la lista de hebras
listaHebras = [];

# Le decimos que funciones se pueden invocar, y con que nombre:
servidorRpc.register_function(crear, "crear")
servidorRpc.register_function(prueba, "prueba")
servidorRpc.register_function(prueba, "desconexion")

# Dejamos que se quede escuchando el servidor RPC:
servidorRpc.serve_forever()
