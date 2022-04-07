
try:
  import usocket as socket
except:
  import socket
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
import webrepl
import network
import esp
import urequests


esp.osdebug(None)
gc.collect()

ssid = ''
password = ''


nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect(ssid, password)


webrepl.start()
