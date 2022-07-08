
from asyncio import events
from importlib.metadata import packages_distributions
from sqlite3 import connect
import subprocess
import threading
import time
import json
import requests

def sendEvent(eventObjectsList):
    
    from clientConnex import p
    for presentResource in range(len(eventObjectsList)):
            strSend = "send -c=110 " + str(eventObjectsList[presentResource])+'\n' #strSend = "send " + resourceList[presentResource]+'\n' #"create 3424"
            p.stdin.write(bytes(strSend,encoding='utf8'))
            p.stdin.flush()


def loadEventList(eventSelection):
    from clientConnex import p
    match eventSelection:
        case"":
            pass
        case "Vélo sorti de la zone autorisée":
            eventObjectsToSend=[3411,3336] #battery, location, failure
        case "Défaillance électrique":
            eventObjectsToSend=[10350,10282] #
        case "Détection de passants":
            eventObjectsToSend=[3432]
        case "Défaillance capteurs":
            eventObjectsToSend=[10282]
        case "éception commande-DownLink":
            eventObjectsToSend=[10350]
        case "Dépassement seuil CO2":
            eventObjectsToSend=[3304,3407]
        case "Niveau de remplissage atteint":
            eventObjectsToSend=[3435]
        case "Dépassement seuil température":
            eventObjectsToSend=[3303]
        case "Baisse niveau carburant":
            eventObjectsToSend=[3435]
        case "Pic de consommation énergétique":
            eventObjectsToSend=[3328]
        
    def addResource_thread():
           
        for objects in eventObjectsToSend:
            strCreate = "create " + str(objects)+'\n' #"create 3424"
            p.stdin.write(bytes(strCreate,encoding='utf8'))
            p.stdin.flush()
    t2 = threading.Thread(target=addResource_thread)
    t2.start()
    return eventObjectsToSend
        
                     
         