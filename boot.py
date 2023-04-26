# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import network
import time

def wifi(WIFI_SSID, WIFI_PASSWORD):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    time.sleep(5)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    time.sleep(5)
    print('config reseau:', wlan.ifconfig())

webrepl.start()
gc.collect()