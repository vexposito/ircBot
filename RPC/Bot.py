import socket
import time
import string # modulo que contiene las secuencias comunes de caracteres ASCII
import random # modulo que se ocupa de la generacion aleatoria
import sqlite3

class Bot:    
      def __init__(self, servidor, canal, nombre, puerto, patron):
            self.irc          = None
            self.servidor     = servidor
            self.canal        = canal
            self.nombre       = nombre
            self.puerto       = puerto
            self.patron       = patron
            capturar          = False 
            self.funcionar    = 1

      def respuesta_ping(self, canal, ircmsg):
            if ircmsg.find("PING :") != -1:
                  respuesta_ping = ircmsg
                  respuesta_ping = respuesta_ping[respuesta_ping.find("PING :"):]
                  respuesta_ping = respuesta_ping.split("\n", 1 )
                  respuesta_ping = respuesta_ping[0].replace("I", "O", 1)
                  self.irc.send(respuesta_ping)
                  self.unirse_a_canal(self.canal)    
                  print "\n\r"
        
      def enviar_mensaje(self, canal, ircmsg):
            self.irc.send("PRIVMSG " + self.canal + " : " + self.ircmsg + "\n\r")            
          
      def unirse_a_canal(self, canal):
            self.irc.send("JOIN " + self.canal + "\n\r")


      def  obtener_nick(self, canal, ircmsg):
            if ircmsg.find("PRIVMSG " + self.canal) != -1:
                  nick = ircmsg.split('!', 1 )
                  nick = nick[0].replace(":", "",1)
                  print(ircmsg + self.canal)
                  return nick                              
            
      def obtener_mensaje(self, canal, ircmsg):
            if ircmsg.find("PRIVMSG " + self.canal) != -1:
                  mensaje = ircmsg.split(self.canal + ' ', 1 )
                  mensaje = mensaje[1].replace(":", " ",1)
                  return mensaje
       
      def mostrar_chat(self, canal, ircmsg):
            print (self.obtener_nick(self.canal, ircmsg) + " : " + self.obtener_mensaje(self.canal, self.ircmsg))

      def existe_ID(self, ID):
            print self.cursor.execute("SELECT ID FROM EVENTO WHERE ID == '" + self.ID + "'")            
            if (self.cursor.fetchone()) != None:
                  return True
            else:
                  return False

      def existe_Bot_ID(self,ID):
            print self.cursor.execute("SELECT ID FROM BOT WHERE ID =='" + self.Bot_ID + "'")
            if(self.cursor.fetchone()) != None:
                  return True
            else:
                  return False

      def generar_event_ID(self):
            probarDeNuevo = True
            while probarDeNuevo:            
                  numerito    = random.choice(range(100))
                  t1          = time.strftime('%H %M %S')
                  t1          = t1.replace(" ", "")
                  self.ID     = 'BOT0' + t1 + str(numerito)
                  if self.existe_ID(self.ID) == False:
                        probarDeNuevo = False
                  else:
                        probarDeNuevo = True                        
            return self.ID

      def generar_Bot_ID(self):
            probarDeNuevo = True
            while probarDeNuevo:            
                  numerito          = random.choice(range(100))
                  self.Bot_ID       = 'BOT_'  + str(numerito)
                  if self.existe_ID(self.Bot_ID) == False:
                        probarDeNuevo = False
                  else:
                        probarDeNuevo = True                        
            return self.Bot_ID

      def analizar_canal(self, canal,ircmsg):
            for i in self.patron:                  
                  if ((ircmsg.find(i)!= -1)):
                        tiempo = time.strftime('%d %b %y / %H:%M:%S \n\r')
                        print '================================ ENCONTRADO ==============================='+ "\n\r"
                        print tiempo + "\n\r" + 'En el canal: ' + self.canal + "\n\r"
                        print 'Se ha encontrado el patron: \'' + i + '\' \n\r'
                        print '==========================================================================='+ "\n\r"
                        ID = self.generar_event_ID()                        
                        self.capturar = True
                        self.cursor.execute (
                              "INSERT INTO EVENTO (ID, FECHA, CANAL, SERVIDOR, PATRON) VALUES ('" 
                              + ID + "' ,'" + tiempo + "' , '" + self.canal + "', '" + self.servidor +"', '" 
                              + i + "')"
                              )
                        self.con.commit()  

      def guardar_msg(self, ircmsg, ID):
            usuario          = self.obtener_nick(self.canal, ircmsg)
            mensaje          = self.obtener_mensaje(self.canal, ircmsg)
            tiempo           = time.strftime('%d %b %y / %H:%M:%S \n\r')
            self.cursor.execute (
                  "INSERT INTO MENSAJES (ID, FECHA, CANAL, SERVIDOR, USUARIO, MENSAJE) VALUES ('" 
                  + ID + "' ,'" + tiempo + "' , '" + self.canal + "', '" + self.servidor + "', '" 
                  + usuario +"', '" + mensaje +"')"
                  )
            self.con.commit()


      #def estado():
      #def estado: dentro de irc en el estado en el que esta - conectado-escuchaando-capturadno..,.,
      #num eventos...,canal,servidor,patron
      #num usuarios en el canal,tiempo conexion,tiempo desde el ultimo patron, BOT_ID
      #Tiempo de conexion en el bot, estado en el que se encuentra

      def desconectarse(self, canal):
            self.funcionar = 0;
            self.irc.send("QUIT" + self.canal + "\n\r")
            print "Desconectado!"
            exit()


      def conexion(self):   
            # print ">> parametros del bot en BOT: "  + " \n\r" +  self.servidor + " \n\r" + self.canal + " \n\r" + self.nombre + " \n\r" + self.puerto + " \n\r" + self.patron + " \n\r"   
            try:
                  self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  print 'Error en la conexion 1'
                  print self.servidor
                  print self.puerto
                  self.irc.connect((self.servidor, self.puerto))
                  print 'Error en la conexion 2'
                  self.irc.send("NICK " + self.nombre +"\r\n")
                  print 'Error en la conexion 3'
                  self.irc.send("USER " + self.nombre + " 0 * : " + self.nombre + "\r\n")
                  print 'Error en la conexion 4'
                  self.irc.send("JOIN : %s \r\n" % self.canal)
                  print 'Error en la conexion 5'
                  #Conexion BD
                  self.con    = sqlite3.connect('irc.db')  #con_bd.close()
                  self.cursor = self.con.cursor()  #cursor.close()
             
            except:
                  print '>> Error en la conexion'
                  exit()


            print ">> Conectando... " + "\n\r"
            self.unirse_a_canal(self.canal)
            time.sleep(4)
            self.unirse_a_canal(self.canal) # REvisar
            print '================================ CONECTADO ================================' + "\n\r"
            print "INFORMACION DE LA SESION" + "\n\r"  + time.strftime('%H:%M:%S / %d %b %y') + "\n\r" + "Canal: " + self.canal + "\n\r" + "Servidor: " + self.servidor + "\n\r"
            print "Patron de busqeda: " + self.patron
            print '===========================================================================' + "\n\r"



            while self.funcionar:
                  contador = 0
                  ircmsg     = self.irc.recv(1024)  
                  print time.strftime('%H:%M:%S \n\r') + ircmsg  + "\n\r"
 
                  if ((ircmsg.find("PING") != -1)):            
                        self.respuesta_ping(self.canal, ircmsg)

                  elif ((ircmsg.find("PRIVMSG") != -1)):            
                        self.analizar_canal(self.canal, ircmsg)
                        if (self.capturar == True):
                              self.guardar_msg(ircmsg, self.ID)
                  else :
                        contador = contador + 1
                        print '>> Mensaje Desconocido'
                        print ircmsg
                        if contador == 100:
                              exit()
                        pass


