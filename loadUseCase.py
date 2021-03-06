
import threading
import settings


def setUsecaseObjects(usecaseSelection):
    from clientConnex import p
    from mainwindow import loadedUseCasesSatus
    eventObjectsToCreate =""
    
    match usecaseSelection:
            case "Bike tracking":
               eventObjectsToCreate=[3333,3336,3411,10282]
            case "Eclairage public":
               eventObjectsToCreate=[3333,3417,3432,10350,10282]    #time, Luminaire asset, ight failiure meter 
            case "Qualité de l'air":
                eventObjectsToCreate=[3333,3303, 3304,3407,10282]
            case "Poubelles intelligentes":
                eventObjectsToCreate=[3333,3435,10282]
            case "Chaîne de froid":
                eventObjectsToCreate=[3333,3336,3411,3435,10282]
            case "Salle hors-sac":
                eventObjectsToCreate=[3328,3333,3435,10282]
    #loadedUseCasesSatus = "YES"

    return eventObjectsToCreate


def loadUseCaseObjects(eventObjectsToCreate):
    from mainwindow import loadedUseCasesSatus
    from clientConnex import p 
    def addResource_thread():
        
        for objects in eventObjectsToCreate:
            strCreate = "create " + str(objects)+'\n' #"create 3424"
            p.stdin.write(bytes(strCreate,encoding='utf8'))
            p.stdin.flush()
            self.dataSentSignal.emit()
    t2 = threading.Thread(target=addResource_thread)
    t2.start()
    loadedUseCasesSatus = "YES"
    return eventObjectsToCreate
    
    
        