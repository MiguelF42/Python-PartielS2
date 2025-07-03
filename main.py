import ports
import ftp
import local
import reseau
from apscheduler.schedulers.background import BackgroundScheduler
from tools import log
from dotenv import load_dotenv
import os 

load_dotenv()  # Charger les variables d'environnement depuis le fichier .env

def printMenu(user) :
    if user == 'paris' :
        printMenuParis()
    else :
        printMenuAutres()

def printMenuParis() : # Menu spécifique pour l'utilisateur de Paris
    print('')
    print('')
    print('==============Toolbox==============')
    print('1. Gestion des utilisateurs')
    print('2. Gestion FTP')
    print('3. Gestion Local')
    print('4. Scan de ports')
    print('5. Scan Réseau')
    print('0. Quitter')
    print('')

def printMenuAutres() : # Menu pour les autres utilisateurs
    print('')
    print('')
    print('==============Toolbox==============')
    print('1. Gestion des utilisateurs')
    print('2. Gestion FTP')
    print('3. Gestion Local')
    print('0. Quitter')
    print('')

def printMenuConnexion(): # Menu de connexion
    print('================Console Utilisateur===============')
    print('')
    print('1 pour se connecter')
    print('0 pour quitter')

def menuConnexion():
    printMenuConnexion()
    choix = input('Choisissez l\'option : ')
    return choix

def scheduledJob():
    ftpsession = ftp.ftpConnexion(os.getenv('FTP_LOG_USER'), os.getenv('FTP_LOG_PASSWORD'))
    if not ftpsession :
        print('Impossible de se connecter au serveur FTP pour le job planifié.')
        return
    log('Job planifié exécuté : sauvegarde des logs')
    print('Job planifié exécuté : sauvegarde des logs')
    ftp.ftpBackupLogs(ftpsession)
    ftpsession.quit()  # Fermer la session FTP après la sauvegarde


scheduler = BackgroundScheduler()
scheduler.add_job(scheduledJob, 'interval', minutes=5)  # Exécute le job toutes les 30 minutes
scheduler.start()

choix = menuConnexion()


while choix != '0':
    connexion = None
    if choix != '1':
        print('Choix incorrect, veuillez réessayer.')
        choix = menuConnexion()
        continue
    
    user = input('Identifiant : ')
    pwd = input('Mot de passe : ')
    connexion = ftp.ftpConnexion(user, pwd)
    if connexion is None:
        print('Identifiant ou mot de passe incorrect.')
        choix = menuConnexion()
        continue

    printMenu(user)
    choixM = input('Choisissez l\'option : ')

    while choixM != '0' :
        if choixM == '1' :
            print('Gestion des utilisateurs')
            log('Gestion des utilisateurs selectionee')
        elif choixM == '2' :
            connexion = ftp.ftpConnexion(user, pwd) # Établir la connexion FTP
            log('Gestion FTP selectionee')
            ftp.ftpMenu(connexion, user, pwd) # Afficher le menu FTP

        elif choixM == '3' :
            log('Gestion Local selectionee')
            local.localMenu(connexion) # Afficher le menu local
        elif choixM == '4' :
            if user != 'paris' : # Vérification si l'utilisateur est Paris
                print('Cette option est réservée aux utilisateurs de Paris.')
                choixM = input('Choisissez l\'option : ')
                continue
            log('Scan de ports selectione')

            ports.scanPortMenu()
        elif choixM == '5' :
            if user != 'paris' : # Vérification si l'utilisateur est Paris
                print('Cette option est réservée aux utilisateurs de Paris.')
                choixM = input('Choisissez l\'option : ')
                continue
            log('Scan Réseau selectione')

            reseau.scanReseauMenu()
        else :
            print('Choix incorrect')
            log('Choix incorrect : ' + choixM)

        printMenu(user)
        choixM = input('Choisissez l\'option : ')

    choix = menuConnexion()