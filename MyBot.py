# -*- coding: cp1252 -*-
import socket
import time
import string # módulo que contiene las secuencias comunes de caracteres ASCII
import random # módulo que se ocupa de la generación aleatoria
 
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
###############################################################################################################################
###############################################################################################################################

 
def respuesta_ping(ircmsg, canal):
      if ircmsg.find("PING : ") != -1:
            respuesta_ping = ircmsg
            respuesta_ping = respuesta_ping[respuesta_ping.find("PING : "):]
            respuesta_ping = respuesta_ping.split("\n", 1 )
            respuesta_ping = respuesta_ping[0].replace("I", "O", 1)
            irc.send(respuesta_ping)
            unirse_a_canal(canal)
            print respuesta_ping
            print "\n\r"
        
def enviar_mensaje(canal , msg):
      irc.sendall("PRIVMSG " + canal + " : " + msg + "\n\r") 
      
      
def unirse_a_canal(canal):
      irc.send("JOIN " + canal + "\n\r")

def desconectarse(canal):
      irc.send("QUIT " + canal + "\n\r")
      
def  obtener_nick(canal, ircmsg):
      if ircmsg.find("PRIVMSG " + canal) != -1:
            nick = ircmsg.split('@', 1 )
            nick = nick[0].replace(" : ", "",1)
            print(ircmsg + canal)
            return nick
      
      
def obtener_mensaje(canal, ircmsg):
      if ircmsg.find("PRIVMSG " + canal) != -1:
            mensaje = ircmsg.split(canal + ' ', 1 )
            mensaje = mensaje[1].replace(" : ", " ",1)
            return mensaje
 
 
def mostrar_chat(ircmsg, canal):
      print (obtener_nick(canal, ircmsg) + " : " + obtener_mensaje(canal, ircmsg))

           
def analizar_canal(canal,ircmsg):
      patron = ['wola', 'qtal']
      global capturar
      for i in patron:                  
            if ((ircmsg.find(i)!= -1)):
                  tiempo = time.strftime('%H:%M:%S / %d %b %y \n\r')
                  print '---------------------------------------------------------------------'+ "\n\r"
                  print tiempo + "\n\r" + 'En el canal: ' + canal + "\n\r"
                  print 'Se ha encontrado el patron: \'' + i + "'\ \n\r"
                  print '---------------------------------------------------------------------'+ "\n\r"
                  capturado = open('capturado.txt', 'w')                 
                  capturado.write(tiempo + '\n\r'  + 'Captura del canal: ' + canal + "\n\r") 
                  capturar = True


def guardar_msg(ircmsg, canal):
      usuario = obtener_nick(canal, ircmsg)
      print '--> El usuario es: ' + usuario + "\n\r" + '--> Escribe: '+ ircmsg + '\n\r'
      capturado = open('capturado.txt', 'a')
      capturado.write("\n\r" + '    ' + usuario + "\n\r" + '      '+ ircmsg + '\n\r')
      capturado.close()


      
###############################################################################################################################
###############################################################################################################################
#ESTABLECIMIENTO DE LA CONEXIÓN
           
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((servidor, puerto))
irc.send("USER "+ nombre +" "+ nombre +" "+ nombre +" \n\r")
irc.send("NICK "+ nombre +"\n\r")
irc.send("NICK %s\r\n" % nombre)
irc.send("USER %s %s bla : %s\r\n" % (nombre, servidor, nombre))
irc.send("JOIN : %s\r\n" % canal)
 
print "Conectando... "+"\n\r"
unirse_a_canal(canal)
time.sleep(4)
unirse_a_canal(canal)
print "¡CONECTADO! " +"\n\r"
print "INFORMACIÓNDE LA SESION" +"\n\r" + time.strftime('%H:%M:%S / %d %b %y')+"\n\r"+ "Canal: " + canal + "\n\r"+ "Servidor: " + servidor + "\n\r"


#time.sleep(5)
#desconectarse(canal)
#print("¡Desconectado! ")

while 1:
      ircmsg = irc.recv(512)
      capturar
      print time.strftime('%H:%M:%S \n\r') + ircmsg  + "\n\r"
#      respuesta_ping(ircmsg,canal)       
      if ((ircmsg.find("PRIVMSG") != -1) != 1):
            respuesta_ping(ircmsg,canal)


      if ((ircmsg.find("PRIVMSG") != -1)):            
            analizar_canal(canal,ircmsg)
            if (capturar == True):
                  guardar_msg(ircmsg, canal
                              )

            





