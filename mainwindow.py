# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from csv import list_dialects
from ctypes.wintypes import LPWIN32_FIND_DATAA
from gc import callbacks
import threading
from time import sleep
from turtle import showturtle
from PyQt5 import QtCore, QtGui, QtWidgets

import settings
import time
from clientConnex import connectIface_function,p
from simulationEvents import sendEvent, loadEventList
from loadUseCase import loadUseCaseObjects
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
from PyQt5.QtWidgets import QApplication

from datetime import datetime  
from TESTLOG import sendPeriod, sendThread
import logging
from lwm2mSniff import lwm2mSniffer


count=0
logging.basicConfig(level=logging.WARNING)
#connexion_status = 'None'logTextToShow#simulationStatus = "OFF"

sentResources=[]
LOGlist = ""
pausedTime ='None'
from IHM import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow       ):

    dataSentSignal = pyqtSignal()    
    startSimulationSignal = pyqtSignal()
    stopSimulationSignal = pyqtSignal()
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.connectClickabales()


    def connectClickabales(self):
         #make drop menus clickabel
        self.useCase_dropBox.activated.connect(self.selectUseCase)
        self.useCase_dropBox.activated.connect(self.setAvailableEvents)
        self.event_dropBox.activated.connect(self.selectEvent)
        
        # link buttons to methods
        self.startSimulation_button.clicked.connect(self.startSimulation_function)
        #self.startSimulation_button.clicked.connect(self.startLOG)   
        self.stopSimulation_Button.clicked.connect(self.stopSimulation_function)
        self.sendEvent_Button.clicked.connect(self.sendEvent_function)

        #add options to drop menu
        self.useCase_dropBox.addItem("")
        self.useCase_dropBox.addItem("Bike tracking")
        self.useCase_dropBox.addItem("Eclairage public")
        self.useCase_dropBox.addItem("Qualité de l'air")
        self.useCase_dropBox.addItem("Poubelles intelligentes")
        self.useCase_dropBox.addItem("Chaîne de froid")
        self.useCase_dropBox.addItem("Salle hors-sac")

        #for tests
        self.sendingDataPeridod_Input.setText("3")

        #connect signals
        self.dataSentSignal.connect(self.showLog)
        self.dataSentSignal.connect(self.measureData)
        self.startSimulationSignal.connect(self.startWatch) 
        self.stopSimulationSignal.connect(self.stopWatch)
        #self.lw_sniffer.newPacketSignal.connect(self.measureData)

        #add logger box

    
    def sendResource_function(self,resourceList):
        from clientConnex import p
        global t6
        #resourceList=[3411,3336,3346,6]
        # if(simulationStatus == "OFF"):
        #     return 0
            
        
        for presentResource in range(len(resourceList)):
                strSend = "send -c=110 " + str(resourceList[presentResource])+'\n' #strSend = "send " + resourceList[presentResource]+'\n' #"create 3424"
                p.stdin.write(bytes(strSend,encoding='utf8'))
                p.stdin.flush()
        #t6.join()        
    
    
    def peridoicMode_fucntion(self,sendingPeriod,simulationDuration): #,sendingDataPeridod_Input,resourceList
        global t6
        
        def periodicMode_thread():
            
            
            global sentResources
            while settings.simulationStatus == "ON" and ((time.time() - simulationStartTime) <= simulationDuration):

                global sentResources
                global LOGlist
                listToSend = loadUseCaseObjects(self.useCase_dropBox.currentText())
                sentResources = listToSend
                
                LOGlist = LOGlist + str(datetime.now())+ " " +str(sentResources) +'\n' + str(time.time() - simulationStartTime)+'\n'
               
                self.dataSentSignal.emit()
                
                self.sendResource_function(listToSend)
                sleep(sendingPeriod)
       
        t6 = threading.Thread(target=periodicMode_thread)
        t6.start()

    def startSimulation_function(self):

        self.startSimulationSignal.emit()
        
        global simulationDuration
        global simulationStartTime
        settings.simulationStatus = "ON"
        if simulationStartTime == 'None':
                simulationStartTime = time.time()
        else:
                simulationStartTime = pausedTime

        simulationDuration = int(self.simulationDuration_Input.text()) #in seconds
        sendingPeriod = int(self.sendingDataPeridod_Input.text())
        resourceList =loadUseCaseObjects(useCaseSelction)
 
        sleep(2)
        listToSend = loadUseCaseObjects(useCaseSelction)
        self.peridoicMode_fucntion(sendingPeriod,simulationDuration)
        
        

    


    def stopSimulation_function(self):
        #global simulationStatus
        self.stopSimulationSignal.emit()
        settings.simulationStatus = "OFF"

        


    def selectUseCase(self):
        global lw_sniffer
        lw_sniffer = self.createSniffer()
        global useCaseSelction
        useCaseSelction = self.useCase_dropBox.currentText()
        

        match useCaseSelction:
            case "Bike tracking":
                self.useCaseDescription_display.setText("This is Bike tracking use case description")
                loadUseCaseObjects("Bike tracking")
            case "Eclairage public":
                self.useCaseDescription_display.setText("This is Chaîne de froid use case description")
                loadUseCaseObjects("Eclairage public")
            case "Qualité de l'air":
                self.useCaseDescription_display.setText("This is Qualité de l'air use case description") 
                loadUseCaseObjects("Qualité de l'air")
            case "Poubelles intelligentes":
                self.useCaseDescription_display.setText("This is Poubelles intelligentes use case description") 
                loadUseCaseObjects("Poubelles intelligentes")
            case "Chaîne de froid":
                self.useCaseDescription_display.setText("This is Chaîne de froid use case description") 
                loadUseCaseObjects("Chaîne de froid")        
            case "Salle hors-sac":
                self.useCaseDescription_display.setText("This is salle hors-sac use case description")    
                loadUseCaseObjects("Salle hors-sac")         


    def setAvailableEvents(self):
        global useCaseSelction
        eventSelection = self.event_dropBox.currentText()
        
        match useCaseSelction:
                case "":
                        self.event_dropBox.clear()
                        self.eventDescription_display.clear()
                        
                case "Bike tracking":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["Vélo sorti de la zone autorisée", "Défaillance électrique",""])
                        
                case "Eclairage public":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["Détection de passants", "Défaillance capteurs", "Réception commande-DownLink",""])
                case "Qualité de l'air":
                         self.event_dropBox.clear()
                         self.event_dropBox.addItems(["Dépassement seuil CO2", "Défaillance capteurs",""])
                case "Poubelles intelligentes":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["Niveau de remplissage atteint", "Défaillance capteurs",""])
                        
                case "Chaîne de froid":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["Dépassement seuil température", "Baisse niveau carburant","défaillance capteurs",""])
                case "Salle hors-sac":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["Pic de consommation énergétique","défaillance capteurs",""])

                

        self.event_dropBox.setCurrentText("")
        
    def selectEvent(self): 
        global eventSelection
        eventSelection = self.event_dropBox.currentText()
        match eventSelection:
                case "":
                         self.eventDescription_display.clear()
                #event Bike tracking
                case "Vélo sorti de la zone autorisée":
                        self.eventDescription_display.setText("Vélo sorti de la zone autorisée description")
                case "Défaillance électrique":
                        self.eventDescription_display.setText("Objets défaillance électrique")
                #events Eclairage public
                case "Détection de passants":
                        self.eventDescription_display.setText("objets detéction de passants")
                case "Défaillance capteurs":
                        self.eventDescription_display.setText("objets défaillance capteurs")
                case "éception commande-DownLink":
                        self.eventDescription_display.setText("objet réception commande")
                #events qualité de l'air
                case "Dépassement seuil CO2":
                        self.eventDescription_display.setText("objet dépassment seuil CO2")
                case "Défaillance capteurs":
                        self.eventDescription_display.setText("objet défaillance capteurs")
                #event poubelles intelligents
                case "Niveau de remplissage atteint":
                        self.eventDescription_display.setText("objets niveau de remlissage")
                case "Défaillance capteurs":
                        self.eventDescription_display.setText("objets défaillance capteurs")
                #event chaine de froid
                case "Dépassement seuil température":
                        self.eventDescription_display.setText("objets seuil de temprérature")
                case "Baisse niveau carburant":
                        self.eventDescription_display.setText("objets niveau de carburant")
                case "défaillance capteurs":
                        self.eventDescription_display.setText("objets défaillance capteur")
                #event salle hors sac
                case "Pic de consommation énergétique":
                        self.eventDescription_display.setText("objet consommation énergétique")
                case "défaillance capteurs":
                        self.eventDescription_display.setText("objets défaillance capteurs")
    
    def sendEvent_function(self):
        global p
        global LOGlist
        if settings.simulationStatus == "ON" and ((time.time() - simulationStartTime) <= simulationDuration): 
                eventSelection = self.event_dropBox.currentText()
        
                eventObjectsToSend = loadEventList(eventSelection)
                sendEvent(eventObjectsToSend)
                LOGlist =  str(datetime.now())+ " " +str(eventObjectsToSend) +'\n' +LOGlist 
                self.dataSentSignal.emit()
    def createSniffer(self):
        global lw_sniffer
        def create_createSniffer_thread():
                lw_sniffer = lwm2mSniffer()
                return lw_sniffer
        snifferthread = threading.Thread(target=create_createSniffer_thread)
        snifferthread.start()
    def snifflwm2m(self):
        global lw_sniffer
        pass

    @QtCore.pyqtSlot()           
    def measureData(self):
        from lwm2mSniff import packetLen_global
        
        #while settings.simulationStatus == "ON" and ((time.time() - simulationStartTime) <= simulationDuration):
        self.dataUsage_display.setText(packetLen_global)
        
        

#     def selectEvent(self):loadEventList
    @QtCore.pyqtSlot()
    def showLog(self):
       global LOGlist
       global count
       global sentResources
       count = count +1
       global lw_sniffer
       self.info_display.setText(LOGlist)
       
    @QtCore.pyqtSlot()
    def stopWatch(self):
        global pausedTime
        pausedTime = time.time()
        return pausedTime

    @QtCore.pyqtSlot()
    def startWatch(self):
        global pausedTime
        global simulationStartTime
        simulationStartTime =  pausedTime
        return simulationStartTime


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    threading.Thread(target=connectIface_function())
    window.show()
    sys.exit(app.exec_())