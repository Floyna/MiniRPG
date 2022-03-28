from gpiozero import LED
from gpiozero import Button
from time import sleep

class Input:
    def __init__(self, button = Button, led = LED, defInput = str):
        self.button = button
        self.led = led
        self.defInput = defInput
        self.active = False

    def CheckPress(self, press = bool):
        if(self.active == False and press == True):
            self.active = True
            self.led.on()
            sleep(1)
            self.led.off()
            self.active = False
    
    def DefInput(self):
        return self.defInput

    def AllumeLed(self):
        self.led.on()
        sleep(1)
        self.led.off()
