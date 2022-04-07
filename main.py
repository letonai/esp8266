# Complete project details at https://RandomNerdTutorials.com
import machine
import os
import urequests
import time
import sys

REMOTE_REPO="https://raw.githubusercontent.com/letonai/esp8266/main/"
LOCAL_VERSION="0.11"

def updateVersion():
  print("Starting update...")
  res = urequests.get(REMOTE_REPO+"main.py")
  new_exec=res.text
  current_exec = open("main.py", "w")
  current_exec.write(new_exec)
  current_exec.flush()
  current_exec.close()
  print("Update Done, restarting...")
  machine.reset()

def checkVersion():
  res = urequests.get(REMOTE_REPO+"version.current")
  remote_version = res.text
  if LOCAL_VERSION != remote_version:
    print("New Version found: "+remote_version)
    updateVersion()
  else:
    print("No updates found!")

RESET_FILE = "reset.now"
led = machine.Pin(1, machine.Pin.OUT)
def web_page():
  if led.value() == 1:
    gpio_state="OFF"
  else:
    gpio_state="ON"
  
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server ver: """+LOCAL_VERSION+"""</h1> 
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p></body></html>"""
  return html

def webServer():
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  if led_on == 6:
      print('LED ON')
      led.value(0)
  if led_off == 6:
      print('LED OFF')
      led.value(1)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 80))
s.listen(5)

while True:
  try:
    f = open(RESET_FILE, "r")
    print("Reset found!")
    os.remove(RESET_FILE)
    checkVersion()
  except OSError:  
    webServer()


    
