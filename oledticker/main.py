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
LOCAL_VERSION="0.095"
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
  oled.text("Version:"+LOCAL_VERSION,0,25)
  oled.show()
  time.sleep(2)
  machine.reset()

def checkVersion():
  oled.fill(0)
  oled.text('Checkin...', 30, 10)
  oled.show()
  res = urequests.get(REMOTE_REPO+"version.current")
  remote_version = res.text
  oled.text('Remote: '+str(remote_version), 30, 10)
  if LOCAL_VERSION != remote_version:
    oled.fill(0)
    oled.text('New Version...'+str(remote_version), 30, 10)
    oled.text('Updating...', 30, 25)
    oled.show()
    updateVersion()
  else:
    oled.fill(0)
    oled.text("No updates found!", 30, 10)
    oled.show()
    time.sleep(2)

secscount=0
while not nic.isconnected():
    oled.fill(0)
    oled.text('Connecting... '+str(secscount), 0, 0)
    secscount=secscount+1
    oled.show() 
    time.sleep(1)
    
checkVersion()

while True:
  oled.fill(0)
  if nic.isconnected():
    oled.text('Connected...', 0, 0)
    oled.show()
    try:
      oled.fill(0)
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