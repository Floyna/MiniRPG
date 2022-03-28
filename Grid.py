from email.policy import default
from pickle import FALSE, TRUE
from random import randint
from re import I
from gpiozero import Buzzer
from gpiozero import LED
from time import sleep
import time

broker = "localhost"
buzzer = Buzzer(12)


xj =0
yj =0
l = [[]]
mort = False
win = False
onPress = False

class Grid:
    
    def __init__(self, x = int, y = int):
        global l
        self.x = x
        self.y = y
        l = [[" " for i in range(x)]for i in range(y)]
        self.serveur = None
        
    def charposition(self, s = str, c = str):
      pos = []
      for n in range(len(s)):
        if s[n] == c:
          pos.append(n)
      return pos
        
    def setXYJ(self, result = str):
        global xj, yj
        #print("substring setX:" + result[self.charposition(result, '(')[0] + 2:self.charposition(result, '-')[0]])
        #print("substring setY:" + result[self.charposition(result, '-')[0] + 1:self.charposition(result, ')')[0] - 2])
        xj = int(result[self.charposition(result, '(')[0] + 2:self.charposition(result, '-')[0]])
        yj = int(result[self.charposition(result, '-')[0] + 1:self.charposition(result, ')')[0] - 2])
            

    def setup(self): 
        global xj,yj, l, win, mort
        l = [[" " for i in range(8)]for i in range(24)]
        
        position = 1
        sortie = 0
        monstres = 0
        murs = 1
        win = False
        mort = False

        for i in range(murs):

            if(sortie>0):
                x = randint(0,len(l)-1)
                y = randint(0,len(l[x])-1)
                while(l[x][y]!=" "):
                    x = randint(0,len(l)-1)
                    y = randint(0,len(l[x])-1)
                
                l[x][y]="S"
                sortie=sortie-1

            if(monstres>0):
                x = randint(0,len(l)-1)
                y = randint(0,len(l[x])-1)
                while(l[x][y]!=" "):
                    x = randint(0,len(l)-1)
                    y = randint(0,len(l[x])-1)
                l[x][y]="M"
                monstres=monstres-1

            x = randint(0,len(l)-1)
            y = randint(0,len(l[x])-1)
            while(l[x][y]!=" "):
                x = randint(0,len(l)-1)
                y = randint(0,len(l[x])-1)
            l[x][y]="X"

            if(position>0):
                while(l[x][y]!=" "):
                    x = randint(0,len(l)-1)
                    y = randint(0,len(l[x])-1)
                l[0][0]="P"
                position = position-1 
                #clientPublisher.publish("raspi", str(x) +"-" + str(y))
                #xj=0
                #yj=0
                
        
        print("Setup ok")

    def gameOver(self):
        global mort
        mort = True
        clientPublisher.publish("gameState", "gameOver")
        callBuzzer()
        print("Pacman est mort")

    def checkCase(self, position):
        global l
        global win
        if position == " ":
            print("La voie est libre")
            return True
        elif position == "X":
            print("Un mur vous bloque le passage")
            callBuzzer()
            return False

        elif position == "M":
            print("Un monstre vous mange")
            self.gameOver()
            return True
        elif position == "S":
            win = True
            clientPublisher.publish("gameState", "gameWin")
            print("Vous êtes sortis du labyrinthe")
            return True
                    


    def show(self):
        global l
        for row in l:
            print(row)

    def mouvement(self, input, distance = int):
        global xj,yj,l, mort, onPress, clientPublisher
        if mort == False:
            
            if input.DefInput() == "Haut":
                for i in range(distance+1):
                    if(i!=0 and xj-i >=0):
                        print(str(i) + l[xj-i][yj])
                        if l[xj-i][yj]!= " ":
                            print( l[xj-i][yj] + " a " + str(i) + " cases")
                            clientPublisher.publish("radar",str(l[xj-i][yj]) + str(xj-i) +"-" +  str(yj))
                            break
                        elif(i!=1):
                            clientPublisher.publish("radar",str(l[xj-i][yj]) + str(xj-i) +"-" +  str(yj))
                        if xj-i ==0:
                            break
                if(xj!=0):
                    if(self.checkCase(l[xj-1][yj])):
                        l[xj][yj]=" "
                        xj=xj-1
                        l[xj][yj] = "P"
                        self.serveur.sendMsg("mouvement " + str(xj) + "-" + str(yj))
                        self.serveur.updatePosBD(str(xj) + "-" + str(yj))
                        input.AllumeLed()
                        
                else:
                    print("Mouvement impossible : limite atteinte")
                    callBuzzer()
            elif input.DefInput()  == "Gauche":
                for i in range(distance+1):
                    if(i!=0 and yj-i >=0):
                        print(str(i) + l[xj][yj-i])
                        if l[xj][yj-i]!= " ":
                            print( l[xj][yj-i] + " a " + str(i) + " cases")
                            clientPublisher.publish("radar",str(l[xj][yj-i]) + str(xj) +"-" +  str(yj-i))
                            break
                        elif(i!=1):
                            clientPublisher.publish("radar",str(l[xj][yj-i]) + str(xj) +"-" +  str(yj-i))
                        if yj-i ==0:
                            break
                if(yj!=0):
                    if(self.checkCase(l[xj][yj-1])):
                        l[xj][yj]=" "
                        yj=yj-1
                        l[xj][yj] = "P"
                        self.serveur.sendMsg("mouvement " + str(xj) + "-" + str(yj))
                        input.AllumeLed()
                    
                        
                    
                else:
                    print("Mouvement impossible : limite atteinte")
                    callBuzzer()
            elif input.DefInput()  == "Bas":
                for i in range(distance+1):
                    if(i!=0 and xj+i <= len(l)-1):
                        print(str(i) + l[xj+i][yj])
                        if l[xj+i][yj]!= " ":
                            print( l[xj+i][yj] + " a " + str(i) + " cases")
                            clientPublisher.publish("radar",str(l[xj+i][yj]) + str(xj+i) +"-" +  str(yj))
                            break
                        elif(i!=1):
                            clientPublisher.publish("radar",str(l[xj+i][yj]) + str(xj+i) +"-" +  str(yj))
                        if xj+i ==len(l)-1:
                            break
                if(xj!=len(l)-1):
                    if(self.checkCase(l[xj+1][yj])):
                        l[xj][yj]=" "
                        xj=xj+1
                        l[xj][yj] = "P"
                        self.serveur.sendMsg("mouvement " + str(xj) + "-" + str(yj))
                        self.serveur.updatePosBD(str(xj) + "-" + str(yj))
                        input.AllumeLed()
                    
                else:
                    print("Mouvement impossible : limite atteinte")
                    callBuzzer()
            elif input.DefInput() == "Droite":
                for i in range(distance +1):
                    if(i!=0 and yj+i<=len(l[xj])-1):
                        print(str(i) + l[xj][yj+i])
                        if l[xj][yj+i]!= " ":
                            print( l[xj][yj+i] + " a " + str(i) + " cases")
                            clientPublisher.publish("radar",str(l[xj][yj+i]) + str(xj) +"-" +  str(yj+i))
                            break
                        elif(i!=1):
                            clientPublisher.publish("radar",str(l[xj][yj+i]) + str(xj) +"-" +  str(yj+i))
                        if yj+i ==len(l[xj])-1:
                            break
                if(yj!=len(l[xj])-1):
                    if(self.checkCase(l[xj][yj+1])):
                        l[xj][yj]=" "
                        yj=yj+1
                        l[xj][yj] = "P"
                        self.serveur.sendMsg("mouvement " + str(xj) + "-" + str(yj))
                        self.serveur.updatePosBD(str(xj) + "-" + str(yj))
                        input.AllumeLed()
                else:
                    print("Mouvement impossible : limite atteinte")
                    callBuzzer()
            
        else:
            print('Impossible, la partie est fini')

def callBuzzer():
    #buzzer.on()
    #sleep(0.3)
    #buzzer.off()
    print("Buzzer off pour les tests")
