# -*- coding: cp1252 -*-
import socket
import time
import string # módulo que contiene las secuencias comunes de caracteres ASCII
import random # módulo que se ocupa de la generación aleatoria
 
servidor    = "irc.irc-hispano.org"
canal       = "#Granada"
nombre      = "Aliiicia"
puerto      = 6667
ident       = "Aliiicia"
realname    = "Aliiicia"
 
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

#Crear lista de n elementos

lista = [ 'tea', 'noe', 'amo', 'oca', 'ley','oso', 'fea','hucha', 'ave','torre',
         'teta','tina','tomo','taco','tela','tiza','tufo','techo','tubo','nuera',
         'nido','niño','nomo','nuca','nilo','nuez','naife','nicho','nube','mar',
         'mito','mono','mama','meca','mulo','mesa','mafia','mecha','mapa','corro',
         'codo','caño','cama','coco','cola','cazo','cafe','coche','cubo','lira',
         'loto','luna','lima','loco','lulu','lazo','lofio','lucha','lupa','suero',
         'soda','ceño','suma','saco','sol','seso','sofa','acecha','sapo','faro',
         'foto','fino','fama','foca','falo','fosa','fofo','ficha','fobia','choro',
         'chuto','chino','chama','chico','chal','choza','chufa','chocho','chipo','pera',
         'pito','pino','puma','boca','pala','peso','bofe','bache','pipa','torero']
 
     

      
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
print "INFORMACIÓNDE LA SESION" +"\n\r" + time.strftime('%H:%M:%S / %d %b %y')+"\n\r"+ "Canal: " + canal + "\n\r"+ "Servidor: " + servidor + "\n\r"


#time.sleep(5)
#desconectarse(canal)
#print("¡Desconectado! ")

while 1:
      ircmsg = irc.recv(512)
      
      if ((ircmsg.find("PRIVMSG") != -1) != 1):
            respuesta_ping(ircmsg,canal)
            obtener_mensaje(canal, ircmsg)
            print ircmsg  + "\n\r" 
            #enviar_mensaje(canal, "Hola")
            #enviar_mensaje(canal,random.choice(lista))
            
            ircmsg = ircmsg.strip('\n\r')


