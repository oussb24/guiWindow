


from sqlite3 import connect
import subprocess
import threading
import time
from datetime import datetime
import json
import requests
#shell process to launch leshan client 
p = 'None'
import os
import settings

import logging
#logVar ="not yet"


logging.basicConfig(format='%(asctime)s %(message)s')

def connectIface_function():
            global p
            if (p =='None'):
                # urn = "java -jar leshan-client-demo.jar "+ "-n "+ "urn:lo:lwm2m:"+ self.connectClient_inputEndPointName.text() +" -i "+ self.connectClient_inputEndPointName.text()+" -p 1d576207727841a7b9aa2a1f24448f86 -u lwm2m.integ.m2m.orange.com"
                # urn = urn.strip('"')
                #p = subprocess.Popen(["java","-jar","leshan-client-demo.jar","-n","urn:lo:lwm2m:"+self.connectClient_inputEndPointName.text(),"-i",self.connectClient_inputEndPointName.text(),"-p","1d576207727841a7b9aa2a1f24448f86","-u","lwm2m.integ.m2m.orange.com"], stdin=subprocess.PIPE,stderr=subprocess.PIPE)
                p = subprocess.Popen("java -jar leshan.jar -u lwm2m.integ.m2m.orange.com -n urn:lo:lwm2m:test -i test -p 1d576207727841a7b9aa2a1f24448f86",stdin=subprocess.PIPE,shell=True)
                print("P TYPE IS" + str(type(p)))
            else:
                print("client already connected")
     
            #connexionSignal.emit()


       
        #def sendResource_thread():





def checkClientConnexion(client_check):
 
        #Registered devices
        url = "https://integ.m2m.orange.com/api/v1/deviceMgt/devices"
        payload={}
        headers = {'X-API-Key': '1d576207727841a7b9aa2a1f24448f86'}
        response = requests.request("GET", url, headers=headers, data=payload,verify =False).text
        response = json.loads(response)
        
        registreredDevices = []

        for element in range(len(response)):
            registreredDevices.append(response[element]['id'])
            registreredDevices[element]=registreredDevices[element].replace("urn:lo:nsid:lwm2m:","")
        #print(registreredDevices)
   
        
        connectedDevices = []
        url_devices = "https://integ.m2m.orange.com/api/v1/deviceMgt/devices/urn:lo:nsid:lwm2m:"
        
        payload = ""
        headers = {'X-API-Key': '1d576207727841a7b9aa2a1f24448f86','Content-Type': 'application/json'}
        
        
        
        for urn in range(len(registreredDevices)):
            response = requests.request("GET", url_devices+registreredDevices[urn], headers=headers, data=payload,verify=False).text
            response = json.loads(response)
            if(response['interfaces'][0]['status'] == 'ONLINE'):
                connectedDevices.append(registreredDevices[urn])
        #print(connectedDevices)
        
        #join list elements for display
        
        if (client_check in connectedDevices):
            return True
        else :
            return False

