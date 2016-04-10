import socket
import time
import string # modulo que contiene las secuencias comunes de caracteres ASCII
import random # modulo que se ocupa de la generacion aleatoria
import sqlite3


class BotClases:    
      def __init__(self, servidor, canal, nombre, puerto, capturar, patron):
            self.irc          = None
            self.servidor     = servidor
            self.canal        = canal
            self.nombre       = nombre
            self.puerto       = puerto
            self.capturar     = capturar
            self.patron       = patron

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

      def desconectarse(self, canal):
            self.irc.send("QUIT " + self.canal + "\n\r")
            
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

      def existe_idev(self, idev):
            print self.cursor.execute("SELECT IDEV FROM EVENTO WHERE IDEV == '" + self.idev + "'")            
            if (self.cursor.fetchone())!= None:
                  return True
            else:
                  return False
                
      def generar_idev(self):
            probarDeNuevo = True
            while probarDeNuevo:            
                  numerito    = random.choice(range(100))
                  t1          = time.strftime('%H %M %S')
                  t1          = t1.replace(" ", "")
                  self.idev        = 'BOT0' + t1 + str(numerito)
                  if self.existe_idev(self.idev) == False:
                        probarDeNuevo = False
                  else:
                        probarDeNuevo = True                        
            return self.idev

      def analizar_canal(self, canal,ircmsg):
            global capturar
            global cursor
            global con
            global idev
            for i in self.patron:                  
                  if ((ircmsg.find(i)!= -1)):
                        tiempo = time.strftime('%d %b %y / %H:%M:%S \n\r')
                        print '================================ ENCONTRADO ==============================='+ "\n\r"
                        print tiempo + "\n\r" + 'En el canal: ' + self.canal + "\n\r"
                        print 'Se ha encontrado el patron: \''+ i + '\' \n\r'
                        print '==========================================================================='+ "\n\r"
                        # Escribir en un txt los mensajes caoturados
                        capturado = open('capturado.txt', 'w')                 
                        capturado.write(tiempo + '\n\r'  + 'Captura del canal: ' + self.canal + "\n\r")
                        # Creamos un IDEV para relacionar las dos tablas con el mismo ID
                        idev = self.generar_idev()                        
                        # Escribir datos en una BD
                        self.capturar = True
                        self.cursor.execute ("INSERT INTO EVENTO (IDEV, FECHA, CANAL, SERVIDOR, PATRON) VALUES ('" + idev + "' ,'" + tiempo + "' , '" + self.canal + "', '" + self.servidor +"', '" + i + "')")
                        self.con.commit()  
                      
      def guardar_msg(self, canal, ircmsg):
            usuario     = obtener_nick(self.canal, self.ircmsg)  #print '--> ' + usuario + "     " + '--> '+ ircmsg + '\n\r'
            capturado   = open('capturado.txt', 'a')
            capturado.write("\n\r" + '    ' + usuario + "\n\r" + '      '+ self.ircmsg + '\n\r')
            capturado.close()

      def guardar_bd(self, canal, ircmsg, idev):
            cursor           = self.cursor
            con              = self.con
            usuario          = self.obtener_nick(self.canal, ircmsg)
            mensaje          = self.obtener_mensaje(self.canal, ircmsg)
            tiempo           = time.strftime('%d %b %y / %H:%M:%S \n\r')
            con              = sqlite3.connect('irc.db')          
            cursor           = con.cursor()  #con.close()
            #print '--> ' + usuario + "     " + '--> '+ self.ircmsg + '\n\r'
            cursor.execute ("INSERT INTO MENSAJES (IDEV, FECHA, CANAL, SERVIDOR, USUARIO, MENSAJE) VALUES ('" + idev + "' ,'" + tiempo + "' , '" + self.canal + "', '" + self.servidor + "', '" + usuario +"', '" + mensaje +"')")
            con.commit()

      def conexion(self):            
            self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.irc.connect((self.servidor, self.puerto))
            self.irc.send("NICK " + self.nombre +"\r\n")
            self.irc.send("USER " + self.nombre + " 0 * : " + self.nombre + "\r\n")
            self.irc.send("JOIN : %s \r\n" % self.canal)

             
            print "Conectando... "+"\n\r"
            self.unirse_a_canal(self.canal)
            time.sleep(4)
            self.unirse_a_canal(self.canal)
            print '================================ CONECTADO ================================' + "\n\r"
            print "INFORMACION DE LA SESION" +"\n\r" + time.strftime('%H:%M:%S / %d %b %y')+"\n\r"+ "Canal: " + self.canal + "\n\r"+ "Servidor: " + self.servidor + "\n\r"
            print '===========================================================================' + "\n\r"

            while 1:
                  self.ircmsg     = self.irc.recv(1024)  
                  #print time.strftime('%H:%M:%S \n\r') + self.ircmsg  + "\n\r"
                  self.con        = sqlite3.connect('irc.db')  #con_bd.close()
                  self.cursor     = self.con.cursor()  #cursor.close()
                  self.capturar   

                  if ((self.ircmsg.find("PING") != -1)):            
                        self.respuesta_ping(self.canal, self.ircmsg)

                  if ((self.ircmsg.find("PRIVMSG") != -1)):            
                        self.analizar_canal(self.canal, self.ircmsg)
                        if (self.capturar == True):
                              self.guardar_bd(self.canal, self.ircmsg, idev)

