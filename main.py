import ports
import ftp
import local
import reseau
from tools import log

def printMenu(user) :
    if user == 'paris' :
        printMenuParis()
    else :
        printMenuAutres()

def printMenuParis() :
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

def printMenuAutres() :
    print('')
    print('')
    print('==============Toolbox==============')
    print('1. Gestion des utilisateurs')
    print('2. Gestion FTP')
    print('3. Gestion Local')
    print('0. Quitter')
    print('')

def printMenuConnexion():
    print('================Console Utilisateur===============')
    print('')
    print('1 pour se connecter')
    print('0 pour quitter')

def menuConnexion():
    printMenuConnexion()
    choix = input('Choisissez l\'option : ')
    return choix

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
            connexion = ftp.ftpConnexion(user, pwd)
            log('Gestion FTP selectionee')
            ftp.ftpMenu(connexion, user, pwd)

        elif choixM == '3' :
            log('Gestion Local selectionee')
            local.localMenu()
        elif choixM == '4' :
            if user != 'paris' :
                print('Cette option est réservée aux utilisateurs de Paris.')
                choixM = input('Choisissez l\'option : ')
                continue
            log('Scan de ports selectione')

            ports.scanPortMenu()
        elif choixM == '5' :
            if user != 'paris' :
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