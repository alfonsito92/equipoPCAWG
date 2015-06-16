#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Se le indica el puerto de envío y lo inicia para cada Bluetooth.
# Saca el RSSI y lo envia.

from BluezInquiry import BluezInquiry
import sys
from subprocess import Popen, PIPE
import threading

# Inquiry de forma infinita
def inquiry(inquirier):
    resultado = None
    while True:
        inquirier.inquiry()
        while inquirier.is_inquiring():
            resultado = inquirier.process_event()
            if(resultado!=None):
                return resultado

# Obtenemos la ID y el puerto por el que se enviaran los datos
port = 58978

# Obtenemos la MAC del dispositivo a partir del ID
mac = None
hci_out = Popen(['hcitool', 'dev'], stdout=PIPE).stdout.readlines()

del hci_out[0]  # 'Devices:\n'

for dev in hci_out:
    opts = dev[1:-1].split('\t')  # Elimino el primer tabulador y \n y divido
    if not opts[0][:3] == "hci":
        continue

    dev_id = opts[0][3:]
    mac = opts[1]
    print("[Bluetooth] Soy " + mac + " (" + dev_id + ")")

    # Inicia el inquiry para este Bluetooth
    inquirier = BluezInquiry(int(dev_id), mac, port)
    result = inquiry(inquirier)
    print "Resultado potencias "+str(result)
