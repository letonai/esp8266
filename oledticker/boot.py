import network
import gc

gc.collect()
ssid = 'Bella'
password = 'BellaGatoSemVergonha'
nic = network.WLAN(network.STA_IF)
nic.active(True)
nic.connect(ssid, password)
