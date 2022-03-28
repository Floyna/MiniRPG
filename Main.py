from gpiozero import LED
from time import sleep
from gpiozero import Buzzer
import threading
from gpiozero import Button
from Serveur import Serveur
from Input import Input

serveur = Serveur("localhost")
serveur.start()
press = False

inputs = [Input(Button(18), LED(17),"Gauche"), Input(Button(25), LED(20), "Droite"),
          Input(Button(23), LED(27), "Haut"),  Input(Button(16), LED(21), "Bas")]

def release():
   global press
   press= False
          
def Check():
   global press
   if(press == False):
         if(inputs[2].button.is_pressed):
            serveur.grid.mouvement(inputs[0], 1)
            #inputs[0].AllumeLed()
            press = True
            inputs[0].button.wait_for_release()
            release()

         elif(inputs[3].button.is_pressed):
            serveur.grid.mouvement(inputs[1], 1)
            #inputs[1].AllumeLed()
            press = True
            inputs[1].button.wait_for_release()
            release()

         elif(inputs[0].button.is_pressed):
            serveur.grid.mouvement(inputs[2], 1)
            #inputs[2].AllumeLed()
            press = True
            inputs[2].button.wait_for_release()
            release()

         elif(inputs[1].button.is_pressed):
            serveur.grid.mouvement(inputs[3], 1)
            #inputs[3].AllumeLed()
            press = True
            inputs[3].button.wait_for_release()
            release()

def thread_mouvement():
      while True:
         Check()

mouvement = threading.Thread(target=thread_mouvement)
mouvement.start()

#go()        

#input("appuyer sur une touche pour quitter \n")
