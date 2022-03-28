import paho.mqtt.client as paho
from ConnexionBD import Database
from Grid import Grid

class Serveur:

    def __init__(self, broker=str):
        self.broker = broker
        self.clientSubscriber = ""
        self.clientPublisher = ""
        self.raspbd = Database("185.212.70.1", "3306", "u421892827_raspberry",
                               "BelleDelphine69", "u421892827_raspberry", self)
        self.grid = None
        self.chaName = ""

    def on_message(self, client, userdata, message):
        print("Message received : " + message.payload.decode("utf-8"))
        if(len(message.payload.decode("utf-8")) > 7):
            if(message.payload.decode("utf-8")[0:7] == "adduser"):
                try:
                    username = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[0]:self.charposition(message.payload.decode("utf-8"), ' ')[1]]
                    password = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[1]:len(message.payload.decode("utf-8"))]
                    self.raspbd.addUser(username, password)
                except:
                    print("addUser : Erreur lors de l'ajout")
                    
            elif(message.payload.decode("utf-8")[0:12] == "addcharacter"):
                try:
                    username = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[0]:self.charposition(message.payload.decode("utf-8"), ' ')[1]]
                    password = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[1]:self.charposition(message.payload.decode("utf-8"), ' ')[2]]
                    characterName = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[2]+1:len(message.payload.decode("utf-8"))]
                    self.raspbd.addCharacter(username, password, characterName)
                except Exception as e:
                    print("addCharacter : Erreur lors de l'ajout \n" + str(e))
            elif(message.payload.decode("utf-8")[0:12] == "getcharacter"):
                try:
                    username = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[0]:self.charposition(message.payload.decode("utf-8"), ' ')[1]]
                    password = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[1]:len(message.payload.decode("utf-8"))]
                    self.raspbd.getCharacter(username, password)
                except Exception as e:
                    print("getCharacter : Erreur \n" + str(e))
            elif(message.payload.decode("utf-8")[0:10] == "getchajson"):
                try:
                    username = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[0]:self.charposition(message.payload.decode("utf-8"), ' ')[1]]
                    password = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[1]:len(message.payload.decode("utf-8"))]
                    self.raspbd.getCharacterJson(username, password)
                except Exception as e:
                    print("getCharacter : Erreur \n" + str(e))
            elif(message.payload.decode("utf-8")[0:9] == "connexion"):
                try:
                    username = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[0]:self.charposition(message.payload.decode("utf-8"), ' ')[1]]
                    password = message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[1]:len(message.payload.decode("utf-8"))]
                    self.raspbd.getuser(username, password)
                except Exception as e:
                    print("connexion : Erreur \n" + str(e))
            elif(message.payload.decode("utf-8") == "startGame"):
                try:
                    self.go()
                except Exception as e:
                    print("startGame : Erreur \n" + str(e))
            elif(message.payload.decode("utf-8")[0:10] == "setChaName"):
                try:
                    self.chaName = str(message.payload.decode("utf-8")[self.charposition(message.payload.decode("utf-8"), ' ')[0] + 1:len(message.payload.decode("utf-8"))])
                    print("chaName:" + self.chaName)
                    self.raspbd.setPos(str(self.chaName))
                except Exception as e:
                    print("setChaName : Erreur \n" + str(e))
                   
                    
    def sendMsg(self, msg = str):
      self.clientPublisher.connect(self.broker)
      self.clientPublisher.publish("raspi", msg)
      self.clientPublisher.disconnect()
      
    def updatePosBD(self, pos = str):
      self.raspbd.updatePos(self.chaName, pos)

    def start(self):
        self.clientSubscriber = paho.Client("client-subscriber")
        self.clientPublisher = paho.Client("client-publisher")
        self.clientSubscriber.on_message = self.on_message
        self.clientSubscriber.connect(self.broker)
        self.clientSubscriber.loop_start()
        self.clientSubscriber.subscribe("raspi")
        
        print("Serveur: start - ok")

    def stop(self):
        self.clientSubscriber.disconnect()
        self.clientSubscriber.loop_stop()
        print("Serveur: stop")

    def charposition(self, s = str, c = str):
        pos = []
        for n in range(len(s)):
            if s[n] == c:
                pos.append(n)
        return pos
        
    def go(self):
      self.grid = Grid(8, 24)
      self.grid.serveur = self
      self.grid.setup()
      self.grid.show()
