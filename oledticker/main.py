# Complete project details at https://RandomNerdTutorials.com
from machine import reset
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import machine
import os
import urequests
import time,gc
import network

nic = network.WLAN(network.STA_IF)
REMOTE_REPO="https://raw.githubusercontent.com/letonai/esp8266/main/oledticker/"
EXCHANGE_URL="https://openexchangerates.org/api/latest.json?app_id=f18ac4164bcc42b08dd0bb833fcdb068&base=USD&symbols=BRL&prettyprint=false&show_alternative=false"
LOCAL_VERSION="0.07"
RESET_FILE = "reset.now"
i2c = I2C(scl=Pin(0), sda=Pin( 2))
oled = SSD1306_I2C(128, 64, i2c)

def updateVersion():
  print("Starting update...")
  res = urequests.get(REMOTE_REPO+"main.py")
  new_exec=res.text
  current_exec = open("main.py", "w")
  current_exec.write(new_exec)
  current_exec.flush()
  current_exec.close()
  oled.fill(0)
  oled.text("Update Done, restarting...",0,10)
  oled.text("Version:"+LOCAL_VERSION,0,20)
  oled.show()
  time.sleep(2)
  machine.reset()

def checkVersion():
  res = urequests.get(REMOTE_REPO+"version.current")
  remote_version = res.text
  if LOCAL_VERSION != remote_version:
    oled.fill(0)
    oled.text('New Version...'+str(remote_version), 0, 0)
    oled.text('Updating...', 30, 10)
    oled.show()
    updateVersion()
  else:
    print("No updates found!")

oled.text('Connecting...', 0, 0)
oled.show()
time.sleep(10)
#if nic.isconnected():
#  checkVersion()

while True:
  if nic.isconnected():
    oled.fill(0)
    oled.text('Connected...', 0, 0)
    oled.show()
    # try:
    #   f = open(RESET_FILE, "r")
    #   print("Reset found!")
    #   os.remove(RESET_FILE)
    #   checkVersion()
    # except OSError:  
    #   print("Error...")
    # gc.collect()
    
    try:
      oled.text('Getting rates..', 0, 0)
      res = urequests.get(EXCHANGE_URL)
      oled.text("DOLAR: "+str(res.json()['rates']['BRL']), 0, 20)
      oled.text('Connected...', 0, 0)
    except:
      oled.text("ERROR",0,20)
      oled.show()
  else:
    oled.text('DISCONNECTED...', 0, 0)
  oled.text(str(LOCAL_VERSION),0,50)
  oled.show()
  time.sleep(10)
  gc.collect()
    

