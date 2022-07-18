
import threading
import settings


def setUsecaseObjects(usecaseSelection):
    from clientConnex import p
    from mainwindow import loadedUseCasesSatus
    eventObjectsToCreate =""
    # 3333 : Time, 33336, location, 3411 Battery, 10282 capteur failure
    # 3417 : config lumiere, 3432 compteur de passage, 10350 eclairage 
    # 3303 : temperature, 3407 : smoke alarm
    # 3435 : niveau de remplissage,
    #3328 : niveau de puissance 
    #
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



    
    
        