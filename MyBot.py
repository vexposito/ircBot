# -*- coding: cp1252 -*-
import socket
import time
import string # módulo que contiene las secuencias comunes de caracteres ASCII
import random # módulo que se ocupa de la generación aleatoria
 
servidor    = "irc.irc-hispano.org"
canal       = "#Melilla"
nombre      = "Sariiita"
puerto      = 6667
ident       = "Sariiita"
realname    = "Sariiita"
canalNuevo  = ['#Malaga', '#Ceuta', '#Cadiz', '#Alicante', '#Canarias']
            #Galicia','#Asturias', '#Murcia', '#Amigos', '#Madrid',
            #Granada', '#Barcelona','#Andalucia']

nombreNuevo = ['#Raquel20', '#Flor20', '#Carlota20', '#Mery20', '#Andrea20', '#Susi20',
               '#Suri20', '#Moni20', '#Ami20', 'Marga20', 'Gracia20', 'Bea20',
               'Andaluza20']
 
def respuesta_ping(ircmsg, canal):
      if ircmsg.find("PING :") != -1:
            respuesta_ping = ircmsg
            respuesta_ping = respuesta_ping[respuesta_ping.find("PING :"):]
            respuesta_ping = respuesta_ping.split("\n", 1 )
            respuesta_ping = respuesta_ping[0].replace("I", "O", 1)
            irc.send(respuesta_ping)
            unirse_a_canal(canal)
            print respuesta_ping
            print "\n\r"
        
def enviar_mensaje(canal , msg):
      irc.send("PRIVMSG "+ canal +" :"+ msg +"\n\r") 
      
      
def unirse_a_canal(canal):
      irc.send("JOIN "+ canal +"\n\r")

def unirse_a_otro_canal(canal):
      
      irc.send("JOIN " + canal +"\n\r")

def desconectarse(canal):
      irc.send("QUIT "+canal +"\n\r")
      
def  obtener_nick(canal, ircmsg):
      if ircmsg.find("PRIVMSG "+canal) != -1:
            nick = ircmsg.split('!', 1 )
            nick = nick[0].replace(":", "",1)
            print(ircmsg + canal)
            return nick
      
      
def obtener_mensaje(canal, ircmsg):
      if ircmsg.find("PRIVMSG "+canal) != -1:
            mensaje = ircmsg.split(canal+' ', 1 )
            mensaje = mensaje[1].replace(":", "",1)
            return mensaje
 
 
def mostrar_chat(ircmsg, canal):
      print (obtener_nick(canal, ircmsg)+": "+obtener_mensaje(canal, ircmsg))

#Lista de palabras que el BOT utilizará aleatoriamente

lista = ['hola', 'pescao', 'holi', 'Chao', 'lunes','martes', 'hoola','nadie aqui', 'xao xao','oloa',
         'oola','holaas','Buenos Dias','Buenas','Hello','Saludops','Hi','Good','good day','helloo',
         'helou','Ola Caracola','Nainonaio','alguien','bonito dia','chao Chao','chao pescao','Lalala','jejejejejeje','jaja',
         'nadi aqui','holoaa','hola amigo','aigo','amigo','what','lololol','saludis','wiiii','wola']

 
      
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((servidor, puerto))
irc.send("USER "+ nombre +" "+ nombre +" "+ nombre +" \n\r")
irc.send("NICK "+ nombre +"\n\r")
irc.send("NICK %s\r\n" % nombre)
irc.send("USER %s %s bla :%s\r\n" % (ident, servidor, realname))
irc.send("JOIN :%s\r\n" % canal)
 
print "Conectando... "+"\n\r"
unirse_a_canal(canal)
time.sleep(4)
unirse_a_canal(canal)
print "¡CONECTADO! " +"\n\r"
print "INFORMACIÓNDE LA SESION" +"\n\r" + time.strftime('%H:%M:%S / %d %b %y')+"\n\r"+ "Canal: " + canal + "\n\r"+ "Servidor: " + servidor + "\n\r" + "Nombre de usuario: " + nombre + "\n\r"


#time.sleep(5)
#desconectarse(canal)
#print("¡Desconectado! ")

while 1:
      ircmsg = irc.recv(512)
      print time.strftime('%H:%M:%S \n\r') + ircmsg  + "\n\r"
       
      if ((ircmsg.find("PRIVMSG") != -1) != 1):
            respuesta_ping(ircmsg,canal)
            #obtener_mensaje(canal, ircmsg)             
            #enviar_mensaje(canal, "Hola")

      #Envia un mensaje aleatorio de una lista     
      #enviar_mensaje(canal,random.choice(lista))
      respuesta_ping(ircmsg,canal)
      irc.send("PING :%s\r\n" % canal)
      print  irc.send("PING :%s\r\n" % canal)
      time.sleep(10)
      
#Si el BOT recibe un mensaje de KILL/QUIT/PART/KICK se reconecta a
#otro canal aleatorio dentro de la lista de canales.
      if ((ircmsg.find("KILL") != -1) != 1):
            canal = random.choice(canalNuevo)
            irc.send("USER "+ nombre +" "+ nombre +" "+ nombre +" \n\r")
            irc.send("NICK "+ nombre +"\n\r")
            irc.send("NICK %s\r\n" % nombre)
            irc.send("USER %s %s bla :%s\r\n" % (ident, servidor, realname))
            irc.send("JOIN :%s\r\n" % canal)

            print "Conectando a otro canal... "+"\n\r"
            unirse_a_otro_canal(canal)
            time.sleep(4)
            unirse_a_otro_canal(canal)
            print "¡CONECTADO! " +"\n\r"
            print "INFORMACIÓNDE LA SESION" +"\n\r" + time.strftime('%H:%M:%S / %d %b %y')+"\n\r"+ "Canal: " + canal + "\n\r"+ "Servidor: " + servidor + "\n\r" + "Nombre de usuario: " + nombre + "\n\r"
      #Enviar un 'hola' repetitivo independientemenente de si recibe o no un PRIVMSG
      enviar_mensaje(canal, "Hola")
      time.sleep(10)
            
      if ((ircmsg.find("QUIT") != -1) != 1):
            canal = random.choice(canalNuevo)
            irc.send("USER "+ nombre +" "+ nombre +" "+ nombre +" \n\r")
            irc.send("NICK "+ nombre +"\n\r")
            irc.send("NICK %s\r\n" % nombre)
            irc.send("USER %s %s bla :%s\r\n" % (ident, servidor, realname))
            irc.send("JOIN :%s\r\n" % canal)

            print "Conectando a otro canal... "+"\n\r"
            unirse_a_otro_canal(canal)
            time.sleep(4)
            unirse_a_otro_canal(canal)
            print "¡CONECTADO! " +"\n\r"
            print "INFORMACIÓNDE LA SESION" +"\n\r" + time.strftime('%H:%M:%S / %d %b %y')+"\n\r"+ "Canal: " + canal + "\n\r"+ "Servidor: " + servidor + "\n\r"+ "Nombre de usuario: " + nombre + "\n\r"
      enviar_mensaje(canal, "Hola")
      time.sleep(10)

      if ((ircmsg.find("KICK") != -1) != 1):
            canal = random.choice(canalNuevo)
            irc.send("USER "+ nombre +" "+ nombre +" "+ nombre +" \n\r")
            irc.send("NICK "+ nombre +"\n\r")
            irc.send("NICK %s\r\n" % nombre)
            irc.send("USER %s %s bla :%s\r\n" % (ident, servidor, realname))
            irc.send("JOIN :%s\r\n" % canal)

            print "Conectando a otro canal... "+"\n\r"
            unirse_a_otro_canal(canal)
            time.sleep(4)
            unirse_a_otro_canal(canal)
            print "¡CONECTADO! " +"\n\r"
            print "INFORMACIÓNDE LA SESION" +"\n\r" + time.strftime('%H:%M:%S / %d %b %y')+"\n\r"+ "Canal: " + canal + "\n\r"+ "Servidor: " + servidor + "\n\r"+ "Nombre de usuario: " + nombre + "\n\r"

      enviar_mensaje(canal, "Hola")
