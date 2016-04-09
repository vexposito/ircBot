import threading
from BotClases import BotClases

patron      = ['qtal', 'wola']
servidor    = "irc.irc-hispano.org"
canal       = "#ircVero"
nombre      = "__Aliiicia36"
puerto      = 6667
capturar    = False

patron1      = ['qtal', 'wola']
servidor1    = "irc.irc-hispano.org"
canal1       = "#ircVeroVero"
nombre1      = "__Aliiicia"
puerto1      = 6667
capturar1    = False

class HebraBot(threading.Thread):
     def __init__(self, servidor, canal, nombre, puerto, capturar, patron):
         super(HebraBot, self).__init__()
         self.bot = BotClases(servidor, canal, nombre, puerto, capturar, patron);

     def run(self):
         self.bot.conexion()


hebraBot1 = HebraBot(servidor, canal, nombre, puerto, capturar, patron)
hebraBot2 = HebraBot(servidor1, canal1, nombre1, puerto1, capturar1, patron1)


hebraBot1.start()
hebraBot2.start()




