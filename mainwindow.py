# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
from site import check_enableusersite
import sys

from csv import list_dialects
from ctypes.wintypes import LPWIN32_FIND_DATAA
from gc import callbacks
import threading
from time import sleep
from turtle import showturtle
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.cbook import silent_list
from matplotlib.pyplot import connect

import settings
import time
from clientConnex import connectIface_function,p
from simulationEvents import sendEvent, loadEventList
from loadUseCase import setUsecaseObjects
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)
from PyQt5.QtWidgets import QApplication

from datetime import datetime  
from TESTLOG import sendPeriod, sendThread
import logging
from lwm2mSniff import lwm2mSniffer



loadedUseCasesSatus = "NO"

count=0
logging.basicConfig(level=logging.WARNING)
#connexion_status = 'None'logTextToShow#simulationStatus = "OFF"

sentResources=[]
LOGlist = ""
pausedTime ='None'
from IHM import Ui_MainWindow





class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    dataSentSignal = pyqtSignal()    
    startSimulationSignal = pyqtSignal()
    stopSimulationSignal = pyqtSignal()
    loadedObjectsSignal = pyqtSignal()
    
    def __init__(self):
        LOGlist=""
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.connectClickabales()
        self.createSniffer()

    def connectClickabales(self):
         #make drop menus clickabel
        #self.dataSentSignal.emit()
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
        self.useCase_dropBox.addItem("Qualit?? de l'air")
        self.useCase_dropBox.addItem("Poubelles intelligentes")
        self.useCase_dropBox.addItem("Cha??ne de froid")
        self.useCase_dropBox.addItem("Salle hors-sac")

        #for tests
        self.sendingDataPeridod_Input.setText("3")
        self.simulationDuration_Input.setText("100")
        #connect signals
        self.dataSentSignal.connect(self.showLog)
        self.dataSentSignal.connect(self.measureData)
        
        self.startSimulationSignal.connect(self.startWatch) 
        self.stopSimulationSignal.connect(self.stopWatch)
       
        #self.lw_sniffer.newPacketSignal.connect(self.measureData)

        #add logger box

    
    def sendResource_function(self,resourceList):
        from clientConnex import p
        
        for presentResource in range(len(resourceList)):
                strSend = "send -c=110 " + str(resourceList[presentResource])+'\n' #strSend = "send " + resourceList[presentResource]+'\n' #"create 3424"
                p.stdin.write(bytes(strSend,encoding='utf8'))
                p.stdin.flush()
                #self.dataSentSignal.emit()

        self.dataSentSignal.emit()
    def loadUseCaseObjects(self,eventObjectsToCreate):
        from mainwindow import loadedUseCasesSatus
        from clientConnex import p 
        def addResource_thread():
            
            for objects in eventObjectsToCreate:
                strCreate = "create " + str(objects)+'\n' #"create 3424"
                p.stdin.write(bytes(strCreate,encoding='utf8'))
                p.stdin.flush()
            #self.dataSentSignal.emit()
        t2 = threading.Thread(target=addResource_thread)
        t2.start()
        loadedUseCasesSatus = "YES"
        return eventObjectsToCreate
    def peridoicMode_fucntion(self,sendingPeriod,simulationDuration): #,sendingDataPeridod_Input,resourceList
        global t6
        
        
        i=0
        def periodicMode_thread():

            global sentResources
            global LOGlist
            previousText = " "
            while settings.simulationStatus == "ON" and ((time.time() - simulationStartTime) <= simulationDuration):
                   
                global sentResources
               
                # LOGlist = LOGlist + str(usecaseSelection) + " objects have been loaded correctly " +'\n'
                # LOGlist = LOGlist + str(objectsToCreate) +'\n'
                if(len(self.useCase_dropBox.currentText())>0):
                    if(self.useCase_dropBox.currentText()!= previousText):
                        usecaseSelection = self.useCase_dropBox.currentText()
                        objectsToCreate = self.loadUseCaseObjects(setUsecaseObjects(usecaseSelection))
                        LOGlist =str(datetime.now())+ " " + "created objects " + str(setUsecaseObjects(self.useCase_dropBox.currentText()))+ '\n' +LOGlist 
                                            #self.dataSentSignal.emit()   
                        self.dataSentSignal.emit()
                        sentResources = objectsToCreate
                        self.sendResource_function(sentResources)#objectsToCreate
                        LOGlist = str(datetime.now())+ " " + "sent successfuly objects" + str(objectsToCreate)+'\n' +LOGlist 
                        self.dataSentSignal.emit()
                        previousText = self.useCase_dropBox.currentText()
                        sleep(sendingPeriod)
                    else:
                        self.dataSentSignal.emit()   
                        sentResources = objectsToCreate
                        self.sendResource_function(sentResources)#objectsToCreate
                        LOGlist = str(datetime.now())+ " " + "sent successfuly objects" + str(objectsToCreate)+'\n' +LOGlist 
                        
                        previousText = self.useCase_dropBox.currentText()
                        sleep(sendingPeriod)
                #LOGlist = LOGlist + str(datetime.now())+ " " +str(sentResources)  + str(time.time() - simulationStartTime) + str(sentResources)+'\n'              
                else:
                    print(len(self.useCase_dropBox.currentText()))
                
                
                
       
        t6 = threading.Thread(target=periodicMode_thread)
        t6.start()

        
    def startSimulation_function(self):
        
        global LOGlist          
        global simulationDuration
        global simulationStartTime
        global usecaseSelection
        settings.simulationStatus = "ON"
        self.startSimulationSignal.emit()
        #lw_sniffer = self.createSniffer()
        #threading.Thread(target=self.checkUseCaseSelection())
        
        sendingPeriod = int(self.sendingDataPeridod_Input.text())
        simulationDuration = int(self.simulationDuration_Input.text())

        usecaseSelection = self.useCase_dropBox.currentText()

        if(usecaseSelection!=""):
            threading.Thread(target=connectIface_function())
            LOGlist = str(datetime.now()) + " LWM2M client connected to LiveObjects" + '\n' + LOGlist 
            self.dataSentSignal.emit()
            sleep(5)
        else:
            self.info_display.setText("Please select use case")   


        if simulationStartTime == 'None':
                simulationStartTime = time.time()
        else:
                simulationStartTime = pausedTime

        self.peridoicMode_fucntion(sendingPeriod,simulationDuration)
        
    def stopSimulation_function(self):
        self.stopSimulationSignal.emit()
        settings.simulationStatus = "OFF"

        
        
    
    def selectUseCase(self):
        global lw_sniffer
        
        global useCaseSelction
        useCaseSelction = self.useCase_dropBox.currentText()
        

        match useCaseSelction:
            case "Bike tracking":
                self.useCaseDescription_display.setText("This is Bike tracking use case description")
                setUsecaseObjects("Bike tracking")
            case "Eclairage public":
                self.useCaseDescription_display.setText("This is Cha??ne de froid use case description")
                setUsecaseObjects("Eclairage public")
            case "Qualit?? de l'air":
                self.useCaseDescription_display.setText("This is Qualit?? de l'air use case description") 
                setUsecaseObjects("Qualit?? de l'air")
            case "Poubelles intelligentes":
                self.useCaseDescription_display.setText("This is Poubelles intelligentes use case description") 
                setUsecaseObjects("Poubelles intelligentes")
            case "Cha??ne de froid":
                self.useCaseDescription_display.setText("This is Cha??ne de froid use case description") 
                setUsecaseObjects("Cha??ne de froid")        
            case "Salle hors-sac":
                self.useCaseDescription_display.setText("This is salle hors-sac use case description")    
                setUsecaseObjects("Salle hors-sac")         


    def setAvailableEvents(self):
        global useCaseSelction
        eventSelection = self.event_dropBox.currentText()
        
        match useCaseSelction:
                case "":
                        self.event_dropBox.clear()
                        self.eventDescription_display.clear()
                        
                case "Bike tracking":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["V??lo sorti de la zone autoris??e", "D??faillance ??lectrique",""])
                        
                case "Eclairage public":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["D??tection de passants", "D??faillance capteurs", "R??ception commande-DownLink",""])
                case "Qualit?? de l'air":
                         self.event_dropBox.clear()
                         self.event_dropBox.addItems(["D??passement seuil CO2", "D??faillance capteurs",""])
                case "Poubelles intelligentes":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["Niveau de remplissage atteint", "D??faillance capteurs",""])
                        
                case "Cha??ne de froid":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["D??passement seuil temp??rature", "Baisse niveau carburant","d??faillance capteurs",""])
                case "Salle hors-sac":
                        self.event_dropBox.clear()
                        self.event_dropBox.addItems(["Pic de consommation ??nerg??tique","d??faillance capteurs",""])

                

        self.event_dropBox.setCurrentText("")
        
    def selectEvent(self): 
        global eventSelection
        eventSelection = self.event_dropBox.currentText()
        match eventSelection:
                case "":
                         self.eventDescription_display.clear()
                #event Bike tracking
                case "V??lo sorti de la zone autoris??e":
                        self.eventDescription_display.setText("V??lo sorti de la zone autoris??e description")
                case "D??faillance ??lectrique":
                        self.eventDescription_display.setText("Objets d??faillance ??lectrique")
                #events Eclairage public
                case "D??tection de passants":
                        self.eventDescription_display.setText("objets det??ction de passants")
                case "D??faillance capteurs":
                        self.eventDescription_display.setText("objets d??faillance capteurs")
                case "??ception commande-DownLink":
                        self.eventDescription_display.setText("objet r??ception commande")
                #events qualit?? de l'air
                case "D??passement seuil CO2":
                        self.eventDescription_display.setText("objet d??passment seuil CO2")
                case "D??faillance capteurs":
                        self.eventDescription_display.setText("objet d??faillance capteurs")
                #event poubelles intelligents
                case "Niveau de remplissage atteint":
                        self.eventDescription_display.setText("objets niveau de remlissage")
                case "D??faillance capteurs":
                        self.eventDescription_display.setText("objets d??faillance capteurs")
                #event chaine de froid
                case "D??passement seuil temp??rature":
                        self.eventDescription_display.setText("objets seuil de tempr??rature")
                case "Baisse niveau carburant":
                        self.eventDescription_display.setText("objets niveau de carburant")
                case "d??faillance capteurs":
                        self.eventDescription_display.setText("objets d??faillance capteur")
                #event salle hors sac
                case "Pic de consommation ??nerg??tique":
                        self.eventDescription_display.setText("objet consommation ??nerg??tique")
                case "d??faillance capteurs":
                        self.eventDescription_display.setText("objets d??faillance capteurs")
    
    def sendEvent_function(self):
        global p
        global LOGlist
        if settings.simulationStatus == "ON" and ((time.time() - simulationStartTime) <= simulationDuration): 
                eventSelection = self.event_dropBox.currentText()
        
                eventObjectsToSend = loadEventList(eventSelection)
                sendEvent(eventObjectsToSend)
                LOGlist =  str(datetime.now())+ " sent successfuly event " +str(eventObjectsToSend) +'\n' + LOGlist   
                self.dataSentSignal.emit()
    def createSniffer(self):
        global lw_sniffer
        def create_createSniffer_thread():
                lw_sniffer = lwm2mSniffer()
                return lw_sniffer
        snifferthread = threading.Thread(target=create_createSniffer_thread)
        snifferthread.start()

    @QtCore.pyqtSlot()           
    def measureData(self):
        from lwm2mSniff import packetLen_global
        
        #while settings.simulationStatus == "ON" and ((time.time() - simulationStartTime) <= simulationDuration):
        self.dataUsage_display.setText(packetLen_global)
        #self.dataUsage_display.setText(str(packet_number))
        
    @QtCore.pyqtSlot()
    def showLog(self):
       global LOGlist
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
    settings.init()
    #threading.Thread(target=connectIface_function())
    window.show()
    
    sys.exit(app.exec_())