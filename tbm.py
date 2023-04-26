import urequests
import ntptime
import time

def dif(t1, t2):
    t1_minutes = t1[0] * 60 + t1[1]
    t2_minutes = t2[0] * 60 + t2[1]
    difference = abs(t1_minutes - t2_minutes)
    return difference


def getbusa():
    ntptime.host = "1.europe.pool.ntp.org"
    ntptime.settime()
    r = urequests.get('http://data.bordeaux-metropole.fr/geojson/process/saeiv_arret_passages?key=BEIJKMNSWZ&datainputs={"arret_id":"B_COMB13"}&attributes=["libelle","hor_app","hor_estime","terminus","vehicule"]')
    busdata = r.json()
    if busdata["features"] == []:
        print("Aucun bus ne passe sur la ligne suivante")
    else:
        vehicule = []
        for vec in busdata["features"]:
            end_time = vec["properties"]["hor_estime"].split("T")[1]
            end_time = end_time.split(":")[0:2]
            t2 = (int(end_time[0]), int(end_time[1]))
            start_time = time.localtime()[3:5]
            t1 = (start_time[0]+1, start_time[1])
            if "11" in vec["properties"]["libelle"]:
                vehicule.append((vec["properties"]["libelle"],vec["properties"]["terminus"],str(dif(t1,t2))))
        return vehicule

import max7219
from machine import Pin, SPI

def rever(s):
    s1 = ''
    for c in s:
        s1 = c + s1
    return s1

spi = SPI(1, baudrate=10000000, polarity=0, phase=0)
display = max7219.Matrix8x8(spi, Pin(15), 2)
display.brightness(1)
display.fill(0)

def afficher(txt):
    display.fill(0)
    msg = rever(txt)
    display.text(msg,0,0,1)
    display.show()

def getbus():
    cy = 60
    while True:
        if cy == 60:
            vecs = getbusa()
            cy = 0
        for i in vecs:
            afficher(i[2])
            time.sleep(2)
            cy += 2
    
