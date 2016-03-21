# -*- coding: cp1252 -*-
#     =====================================================================================================================     #
#     ==================================================== IMPORT =========================================================     #
#     =====================================================================================================================     #

import socket
import time
import string # módulo que contiene las secuencias comunes de caracteres ASCII
import random # módulo que se ocupa de la generación aleatoria
import sqlite3

#     =====================================================================================================================     #
#     ============================================ DEFINICION DE VARIABLES ================================================     #
#     =====================================================================================================================     #

servidor    = "irc.irc-hispano.org"
canal       = "#ircVero"
nombre      = "__Aliiicia36"
puerto      = 6667
#ident       = "__Aliiicia"
#realname    = "__Aliiicia"
capturar    = False
nombreNuevo = ['#Raquel20', '#Flor20', '#Carlota20', '#Mery20', '#Andrea20', '#Susi20',
               '#Suri20', '#Moni20', '#Ami20', 'Marga20', 'Gracia20', 'Bea20',
               'Andaluza20']

      
#     =====================================================================================================================     #
#     ============================================ DEFINICION DE FUNCIONES ================================================     #
#     =====================================================================================================================     #
 
def respuesta_ping(canal, ircmsg):
      if ircmsg.find("PING :") != -1:
            respuesta_ping = ircmsg
            respuesta_ping = respuesta_ping[respuesta_ping.find("PING :"):]
            respuesta_ping = respuesta_ping.split("\n", 1 )
            respuesta_ping = respuesta_ping[0].replace("I", "O", 1)
            irc.send(respuesta_ping)
            unirse_a_canal(canal)    
            print "\n\r"
        
def enviar_mensaje(canal , ircmsg):
      irc.send("PRIVMSG " + canal + " : " + ircmsg + "\n\r") 
      
      
def unirse_a_canal(canal):
      irc.send("JOIN " + canal + "\n\r")

def desconectarse(canal):
      irc.send("QUIT " + canal + "\n\r")
      
def  obtener_nick(canal, ircmsg):
      if ircmsg.find("PRIVMSG " + canal) != -1:
            nick = ircmsg.split('!', 1 )
            nick = nick[0].replace(":", "",1)
            print(ircmsg + canal)
            return nick
      
      
def obtener_mensaje(canal, ircmsg):
      if ircmsg.find("PRIVMSG " + canal) != -1:
            mensaje = ircmsg.split(canal + ' ', 1 )
            mensaje = mensaje[1].replace(":", " ",1)
            return mensaje
 
 
def mostrar_chat(canal, ircmsg):
      print (obtener_nick(canal, ircmsg) + " : " + obtener_mensaje(canal, ircmsg))

           
def analizar_canal(canal,ircmsg):
      patron = ['wola', 'qtal']
      global capturar
      global cursor
      global con
      for i in patron:                  
            if ((ircmsg.find(i)!= -1)):
                  tiempo = time.strftime('%H:%M:%S / %d %b %y \n\r')
                  print '================================ ENCONTRADO ==============================='+ "\n\r"
                  print tiempo + "\n\r" + 'En el canal: ' + canal + "\n\r"
                  print 'Se ha encontrado el patron: \''+ i + '\' \n\r'
                  print '==========================================================================='+ "\n\r"
                  # Escribir en un txt los mensajes caoturados
                  capturado = open('capturado.txt', 'w')                 
                  capturado.write(tiempo + '\n\r'  + 'Captura del canal: ' + canal + "\n\r")
                  # Creamos un IDEV para relacionar las dos tablas con el mismo ID
                  
                  
                  # Escribir datos en una BD
                  capturar = True
                  cursor.execute ("INSERT INTO EVENTO (IDEV, FECHA, CANAL, SERVIDOR, PATRON) VALUES ('" + tiempo + "' , '" + canal + "', '" + servidor +"', '" + i + "')")
                  con.commit()
    
                

def guardar_msg(canal, ircmsg):
      usuario = obtener_nick(canal, ircmsg)
      #print '--> ' + usuario + "     " + '--> '+ ircmsg + '\n\r'
      capturado = open('capturado.txt', 'a')
      capturado.write("\n\r" + '    ' + usuario + "\n\r" + '      '+ ircmsg + '\n\r')
      capturado.close()

def guardar_bd(canal, ircmsg):
      usuario = obtener_nick(canal, ircmsg)
      tiempo = time.strftime('%H:%M:%S / %d %b %y \n\r')
      con = sqlite3.connect('irc.db')
      #con_bd.close()
      cursor = con.cursor()
      #cursor_agenda.close()
      cursor.execute ("INSERT INTO MENSAJES (IDEV, FECHA, CANAL, SERVIDOR, USUARIO, MENSAJE) VALUES ('" + tiempo + "' , '" + canal + "', '" + servidor + "', '" + usuario +"', '" + ircmsg +"')")
      con.commit()


      
#     =====================================================================================================================     #
#     ========================================= ESTABLECIMIENTO DE LA CONEXIÓN ============================================     #
#     =====================================================================================================================     #

           
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((servidor, puerto))
#time.sleep(10)
irc.send("NICK "+ nombre +"\r\n")
irc.send("USER " + nombre + " 0 * : " + nombre + "\r\n")
#time.sleep(10)
irc.send("JOIN : %s \r\n" % canal)


#irc.send("USER "+ nombre +" "+ nombre +" "+ nombre + "\r\n")
#irc.send("NICK %s\r\n" % nombre)
#irc.send("USER %s %s bla : %s\r\n" % (nombre, servidor, nombre))

 
print "Conectando... "+"\n\r"
unirse_a_canal(canal)
time.sleep(4)
unirse_a_canal(canal)
print '================================ CONECTADO ================================' + "\n\r"
#print "¡CONECTADO! " +"\n\r"
print "INFORMACIÓNDE LA SESION" +"\n\r" + time.strftime('%H:%M:%S / %d %b %y')+"\n\r"+ "Canal: " + canal + "\n\r"+ "Servidor: " + servidor + "\n\r"
print '===========================================================================' + "\n\r"
#time.sleep(5)
#desconectarse(canal)
#print("¡Desconectado! ")
#respuesta_ping(ircmsg,canal)

#     =====================================================================================================================     #
#     ================================================ TRABAJANDO =========================================================     #
#     =====================================================================================================================     #

while 1:
      ircmsg = irc.recv(512)
      #print time.strftime('%H:%M:%S \n\r') + ircmsg  + "\n\r"
      con = sqlite3.connect('irc.db')
      #con_bd.close()
      cursor = con.cursor()
      #cursor.close()
      capturar
      #respuesta_ping(canal, ircmsg)

      if ((ircmsg.find("PING") != -1)):            
            respuesta_ping(canal, ircmsg)

      if ((ircmsg.find("PRIVMSG") != -1)):            
            analizar_canal(canal,ircmsg)
            if (capturar == True):
                  #guardar_msg(canal,ircmsg)
                  guardar_bd(canal,ircmsg)






