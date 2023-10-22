# Unihiker board Traffic Light
# Roni Bandini, October  2023
# Buenos Aires, Argentina

import time
from pinpong.board import *
from pinpong.extension.unihiker import *
from unihiker import GUI
from unihiker import Audio
import subprocess
import requests


gui = GUI()
Board().begin()

print("No helmet no green - Traffic Light Module")
print("@RoniBandini - October 2023")
print("")

currentLight="green"
waitTime=6
detectionLimit=0.5
noHelmet=0
serverUrl='http://YourServer/YourFolder/'

def updateTrafficLight():

    global currentLight

    gui.clear()

    noHelmet=0

    if currentLight=="green":

        print("Yellow")
        currentLight="yellow"
        img = gui.draw_image(x=0, y=0, w=240, h=320, image='/home/traffic/images/yellow.png')
        gui.draw_text(x = 120,y=260,text="Missing helmet: "+str(int(noHelmet*100))+" %", font_size=10, color="black", origin='top')
        time.sleep(waitTime/2)

        gui.clear()
        print("Red light")
        currentLight="red"
        img = gui.draw_image(x=0, y=0, w=240, h=320, image='/home/traffic/images/red.png')
        gui.draw_text(x = 120,y=260,text="Missing helmet: "+str(int(noHelmet*100))+" %", font_size=10, color="black", origin='top')
        time.sleep(waitTime)

    elif currentLight=="red":

        # read helmet detection rate from server
        print("Getting inference from server...")
        r = requests.get(serverUrl+'helmet.ini')
        noHelmet=r.json()
        print("There are "+str(noHelmet*100)+"% of a rider not wearing a helmet")

        if float(noHelmet)>detectionLimit:
            img = gui.draw_image(x=0, y=0, w=240, h=320, image='/home/traffic/images/nohelmet.png')

        # loop until helmet is on
        while float(noHelmet)>detectionLimit:

            r = requests.get(serverUrl+'helmet.ini')
            noHelmet=r.json()
            print("There are "+str(noHelmet*100)+"% of a rider not wearing a helmet")
            time.sleep(3)

        print("Yellow light")
        currentLight="yellow"
        img = gui.draw_image(x=0, y=0, w=240, h=320, image='/home/traffic/images/yellow.png')
        gui.draw_text(x = 120,y=260,text="Missing helmet: "+str(int(noHelmet*100))+" %", font_size=10, color="black", origin='top')
        time.sleep(waitTime/2)

        gui.clear()
        print("Green light")
        currentLight="green"
        img = gui.draw_image(x=0, y=0, w=240, h=320, image='/home/traffic/images/green.jpg')
        gui.draw_text(x = 120,y=260,text="Missing helmet: "+str(int(noHelmet*100))+"%", font_size=10, color="black", origin='top')
        time.sleep(waitTime)

# main loop

while True:

    updateTrafficLight()
    time.sleep(1)
