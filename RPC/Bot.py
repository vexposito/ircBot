#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: 850 -*-
import socket
import time
import string # modulo que contiene las secuencias comunes de caracteres ASCII
import random # modulo que se ocupa de la generacion aleatoria
import sqlite3

class Bot:    
      def __init__(self, servidor, canal, nombre, puerto, patron, ID_Bot, ID_convers):
            self.irc          = None
            self.servidor     = servidor
            self.canal        = canal
            self.nombre       = nombre
            self.puerto       = puerto
            self.patron       = patron
            self.patron       = self.patron.split(',')
            self.ID_Bot       = ID_Bot
            self.ID_event     = 0
            self.ID_Convers   = ID_convers
            self.tiempo       = time.localtime()
            self.capturar     = False 
            self.funcionar    = 1
            self.credito      = 0


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


      def obtener_nick(self, canal, ircmsg):
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
            print self.cursor.execute("SELECT ID_EVENT FROM EVENTO WHERE ID_EVENT == '" + self.ID_event + "'")            
            if (self.cursor.fetchone()) != None:
                  return True
            else:
                  return False

      def generar_ID_event(self):
            probarDeNuevo = True
            while probarDeNuevo:            
                  numerito    = random.choice(range(100))
                  t1          = time.strftime('%H %M %S')
                  t1          = t1.replace(" ", "")
                  self.ID_event = self.ID_Bot + "_" + t1 + str(numerito)
                  if self.existe_ID(self.ID_event) == False:
                        probarDeNuevo = False
                  else:
                        probarDeNuevo = True                        
            return self.ID_event

      def generar_ID_convers(self):
            t1          = time.strftime('%H %M %S')
            t1          = t1.replace(" ", "")
            self.ID_convers = t1

            # Almacenar numero de conversacion
            self.cursor.execute (
                  " UPDATE BOT_INFO SET ID_CONVERS = ' " + str(self.ID_Bot) 
                  + "'  WHERE ID_CONVERS = '" + str(self.ID_convers) +  "' "
                  )
            self.con.commit()



            return self.ID_convers

      # def existe_ID_Bot(self,ID):
      #       print self.cursor.execute("SELECT ID FROM BOT WHERE ID =='" + self.ID_Bot + "'")
      #       if(self.cursor.fetchone()) != None:
      #             return True
      #       else:
      #             return False


      # def generar_ID_Bot(self):
      #       probarDeNuevo = True      ñ ´
      #       while probarDeNuevo:            
      #             numerito            = random.choice(range(100))
      #             self.ID_Bot         = 'BOT_'  + str(numerito)
      #             if self.existe_ID(self.ID_Bot) == False:
      #                   probarDeNuevo = False
      #             else:
      #                   probarDeNuevo = True                        
      #       return self.ID_Bot


      def analizar_canal(self, canal,ircmsg):       
            eventos = 0            
            for i in self.patron:  
                  mensaje = self.obtener_mensaje(self.canal, ircmsg)
                  # mensaje = str(mensaje)
                  print "comparo -" + mensaje + "- con la palabra de nuestro patron: " + i     
                  if ((mensaje.find(i)!= -1)):
                        self.credito      = self.credito + 5
                        print ">>----------> credito sumado: " + str(self.credito)
                        self.tiempo       = time.time()
                        self.ID_event     = self.generar_ID_event()

                        # self.gestionar_creditos(self.credito, self.tiempo, ircmsg, self.ID_event)
                        tiempo_almacenar  = time.strftime('%d %b %y / %H:%M:%S')

                        print '================================ ENCONTRADO ==============================='+ "\n\r"
                        print str(tiempo_almacenar) + "\n\r" + 'En el canal: ' + str(self.canal) + "\n\r"
                        print 'Se ha encontrado el patron: \'' + i + '\' \n\r'
                        print '==========================================================================='+ "\n\r"
                        self.capturar     = True
                        eventos           = eventos + 1

                        # Anade a la base de datos del registro de los Bot un nuevo evento
                        self.cursor.execute (
                              " UPDATE BOT_INFO SET ID_BOT = ' " + str(self.ID_Bot) + "'  WHERE EVENTOS = '" + str(eventos) + "'"
                              )
                        # Almacena en la base de datos el evento capturado
                        self.cursor.execute (
                              "INSERT INTO EVENTO (ID_EVENT, FECHA, CANAL, SERVIDOR, PATRON) VALUES ('" 
                              + self.ID_event + "' ,'" + tiempo_almacenar + "' , '" + self.canal + "', '" + self.servidor +"', '" 
                              + i + "')"
                              )
                        self.con.commit() 
            self.gestionar_creditos(self.credito, self.tiempo, self.ID_event, ircmsg, self.canal)
            print ">>----------> nos queda \'" + str(self.credito) + "\' creditos"


      def gestionar_creditos(self, credito, tiempo, ID_event, ircmsg, canal):
            hace_falta_nuevo_IDconvers = True
            if self.credito > 0 : 
                  if hace_falta_nuevo_IDconvers:
                        hace_falta_nuevo_IDconvers = False
                        self.generar_ID_convers()
                  if self.capturar:
                        self.guardar_msg(ircmsg, self.ID_event, self.ID_convers)
                  self.credito = self.credito - 1
                  print "guardo msgs..." + str(self.credito) 
                  tiempo_inicio     = self.tiempo
                  tiempo_actual     = time.time()  # cada cuanto se calcula el timepo
                  tiempo_pasa2      = tiempo_actual - tiempo_inicio
                  tiempo           = time.strftime('%M:%S')

                  if tiempo_pasa2 >= 10 : 
                        if self.credito > 0 :                         
                              self.capturar = True                              
                              self.credito = self.credito - 1
                              print "tiempo pasa... " + str(self.credito)                  
                        else :
                              self.capturar = False
                              # self.analizar_canal(self.canal, ircmsg)
                              print "me quedo escuchando..."
                  return self.credito
            else:
                  hace_falta_nuevo_IDconvers = True


                  
            # tiempo entre palabras, tiempo entre el ultimo mensaje, numero palabras encontradas,
            # Asignar credito entre palabras
            # contador con el numero de palabras que voy encontrando
            # 


      def guardar_msg(self, ircmsg, ID_event, ID_convers):
            usuario          = self.obtener_nick(self.canal, ircmsg)
            mensaje          = self.obtener_mensaje(self.canal, ircmsg)
            tiempo           = time.strftime('%d %b %y / %H:%M:%S')
            self.conectar_DB()
            self.cursor.execute (
                  "INSERT INTO MENSAJES (ID_MSG, FECHA, CANAL, SERVIDOR, USUARIO, MENSAJE) VALUES ('" 
                  + self.ID_event + "' ,'" + tiempo + "' , '" + self.canal + "', '" + self.servidor + "', '" 
                  + usuario +"', '" + mensaje +"')"
                  )
            self.con.commit()

      def desconexion(self, ID_Bot, canal):
            self.funcionar = 0;
            self.irc.send("QUIT" + self.canal + "\n\r")
            tiempo         = time.strftime('%d %b %y / %H:%M:%S')
            estado         = "OFF"
            eventos        = 0   

            # self.cursor.execute (
            #       " UPDATE BOT_INFO SET ID_BOT = ' " + str(self.ID_Bot) 
            #       + "'  WHERE EVENTOS = '" + str(eventos) + "', ULTIMA = '" 
            #       + str(tiempo) + "' "
            #       )
            self.con.commit()
            print ">> Desconectado BOT: !" + self.ID_Bot
            exit()

            print ">> ADIOS <<"
            exit()

      def estado(self):
            print ">> Estado del BOT: " + self.ID_Bot
      # dentro de irc en el estado en el que esta - conectado-escuchaando-capturadno..,.,
      # num eventos...,canal,servidor,patron
      # num usuarios en el canal,tiempo conexion,tiempo desde el ultimo patron, ID_Bot
      # Tiempo de conexion en el bot, estado en el que se encuentra


      def conectar_DB(self):
          reintentar = True
          while reintentar: 
              try:         
                  self.con        = sqlite3.connect('C:/Users/vexpo/Desktop/PROYECTO/Django-master/irc.db')  #con_bd.close()
                  self.cursor     = self.con.cursor()  #cursor.close()
                  reintentar = False
                  print ">> OK!  DB Abierta."
              except:
                  reintentar = True
                  cont = 0
                  if cont == 5:
                        cursor.close()
                        exit()
                        print " No ha sido posible establecer conexión. "
                  else:
                        print " ERROR!(Bot) Reintentando conexion con la DB."
                        cont = cont + 1

      def cerrar_DB(self):
          print "Cerrando DB..."
          self.cursor.close()
          self.con.close()

      def conexion(self):   
            print ">> parametros del bot en BOT: "  + " \n\r" +  str(self.servidor) + " \n\r" +  str(self.canal) + " \n\r" + str(self.nombre) + " \n\r" + str(self.puerto) + " \n\r" + str(self.patron) + " \n\r"   
            try:
                  self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                  print ' >> .Socket'
                  self.irc.connect((self.servidor, self.puerto))
                  print ' >> .Connect'
                  self.irc.send("NICK " + self.nombre + "\r\n")
                  print ' >> NICK'
                  self.irc.send("USER " + self.nombre + " 0 * : " + self.nombre + "\r\n")
                  print ' >> USER'
                  self.irc.send("JOIN : %s \r\n" % self.canal)
                  print ' >> JOIN canal'
                  self.conectar_DB()
             
            except:
                  print '>> Error en la conexion con el IRC' + exit()


            print ">> Conectando... " + "\n\r"
            self.unirse_a_canal(self.canal)
            time.sleep(4)
            self.unirse_a_canal(self.canal) # REvisar
            print '================================ CONECTADO ================================' + "\n\r"
            print "INFORMACION DE LA SESION" + "\n\r"  + time.strftime('%H:%M:%S / %d %b %y') + "\n\r" + "Canal: " + self.canal + "\n\r" + "Servidor: " + self.servidor + "\n\r"
            print "Patron de busqeda: " + str(self.patron)
            print '===========================================================================' + "\n\r"


            while self.funcionar:
                  contador   = 0
                  ircmsg     = self.irc.recv(1024)  
                  print time.strftime('%H:%M:%S \n\r') + ircmsg  + "\n\r"
 
                  if ((ircmsg.find("PING") != -1)):            
                        self.respuesta_ping(self.canal, ircmsg)

                  elif ((ircmsg.find("PRIVMSG") != -1)):            
                        self.analizar_canal(self.canal, ircmsg)
 
                  else :
                        contador = contador + 1
                        print '>> Mensaje Desconocido'
                        print ircmsg
                        if contador == 100:
                              exit()
                        pass



