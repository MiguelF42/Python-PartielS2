import socket  
import datetime
import time
import threading
import re

# Fonction pour afficher le menu principal
def print_menu():
    print('')
    print('1. Scan d\'un port spécifique')
    print('2. Scan d\'une plage de ports')
    print('3. Scan de tous les ports')
    print('0. Quitter')

# Fonction pour choisir un port spécifique
def choose_port():

    # Demande à l'utilisateur de saisir un numéro de port
    port = input('Entrez un numéro de port (1-65535): ')

    # Vérification que le port est un nombre entre 1 et 65535
    while not port.isdigit() or int(port) < 1 or int(port) > 65535:

        # Si le port n'est pas valide, on demande à l'utilisateur de le ressaisir
        print('Le numéro de port est invalide. Veuillez entrer un nombre entre 1 et 65535.')
        port = input('Entrez un numéro de port (1-65535): ')

    # On convertit le port en entier et on le retourne
    return int(port)

# Fonction pour choisir une plage de ports
def choose_range():

    # Demande à l'utilisateur de saisir une plage de ports
    port_range = input('Entrez une plage de port (ex: 20-80): ')

    # Vérification que la plage de ports est valide
    while '-' not in port_range or not all((part.isdigit() or int(part) < 1 or int(part) > 65535) for part in port_range.split('-')):
        
        # Si la plage de ports n'est pas valide, on demande à l'utilisateur de la ressaisir
        print('Le format est invalide. Veuillez entrer une plage de port valide (ex: 20-80).')
        port_range = input('Entrer une plage de port valide (ex: 20-80): ')

    # On sépare les deux numéros de port et on les convertit en entiers
    numbers = port_range.split('-')
    start_port = int(numbers[0])
    end_port = int(numbers[1])

    # On retourne la plage de ports sous forme de liste d'entiers
    return [start_port, end_port]

# Fonction pour choisir une adresse IP
def choose_ip():

    # Demande à l'utilisateur de saisir une adresse IP
    ip = input('Entrer une adresse IP (ex: 192.168.1.1): ')

    #REGEX pour vérifier si l'IP est valide
    ipv4_pattern = "r\b(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    
    if len(ip) == 0: # On vérifie si l'utilisateur n'a pas saisi d'IP
        # Si l'utilisateur n'a pas saisi d'IP, on lui attribue une valeur par défaut
        ip = '127.0.0.1'

    # Vérification que l'IP est valide
    while re.match(ipv4_pattern, ip):

        # Si l'IP n'est pas valide, on demande à l'utilisateur de la ressaisir
        print('Adresse IP invalide. Entrer une adresse IP valide (ex: 192.168.1.1).')
        ip = input('Entrer une adresseIP (default : 127.0.0.1) :')

    # on retourne l'IP
    return ip

# Fonction pour choisir le protocole de transport
def choose_transport_protocol():

    # Affichage des options
    print('1. TCP')
    print('2. UDP')

    # Demande à l'utilisateur de choisir un protocole de transport
    protocol = input('Choisissez le protocol de transport (1 or 2): ')

    # Vérification que le choix est valide
    while protocol not in ['1', '2']:

        # Si le choix n'est pas valide, on demande à l'utilisateur de le ressaisir
        print('Choix invalide. Veuillez entrer 1 pourt TCP ou 2 pour UDP.')
        protocol = input('Choisissez le protocol de transport (1 or 2): ')

    # On fait correspondre le choix au protocole de transport approprié
    # SOCK_STREAM pour TCP et SOCK_DGRAM pour UDP
    return socket.SOCK_STREAM if protocol == '1' else socket.SOCK_DGRAM

# Fonction pour afficher l'en-tête de scan
def print_header_scanning(f, protocol, ip, port):
    #  pour la date utiliser ceci
    now=datetime.datetime.now().date()
    print("Date :", now.strftime('%A %d %B %y')) ### à la C date formatée

    ''' %A	Nom complet du jour de la semaine.
    %d	Jour du mois [ 01-31 ].
    %B	Nom complet du mois.
    %y	Année à 2 chiffres [ 00,99 ].
     '''
    ### ou bien sans formatage print("Date:",now) 

    #  pour la date et le temps au même temps utiliser ceci
    now1=datetime.datetime.now().time()
    print("Horaire :", now1.strftime('%H:%M:%S'))

    ''' %H	Heure au format 24 heures [ 00-23 ].
    %M	Minute [ 00-59 ].
    %S	Seconde [ 00-61 ]. La plage des secondes  '''

    print(' ')

    protocol = "TCP" if protocol == 1 else "UDP"
    f.write("Date : "+now.strftime('%A %d %B %y')+"\n")
    f.write("Horaire : "+now1.strftime('%H:%M:%S')+"\n")
    f.write("Début du scan de l'ip "+ip+" sur le ou les port(s) "+port+" en "+protocol+"\n")

# Fonction pour scanner un port spécifique
def scan_port(port,ip, protocol,f):
    try :
        # Création d'une socket pour le scan de port
        connexion_principale = socket.socket(socket.AF_INET, protocol)

        # Définition d'un timeout pour le socket
        connexion_principale.settimeout(1)

        if protocol == socket.SOCK_STREAM: # TCP

            # Connexion à l'adresse IP et au port spécifié
            connexion_principale.connect((ip, port))    

        else: # UDP

            # Envoi d'un paquet vide pour vérifier si le port est ouvert
            connexion_principale.sendto(b'', (ip, port))

            # Attente d'une réponse
            connexion_principale.recvfrom(1024)

        # Si la connexion réussit, le port est ouvert    
        print("Le port",port," est ouvert")
        f.write("Port "+str (port)+ " => ouvert \n")
       
    except:
        # Si une exception se produit, le port est fermé ou injoignable
        print ("Le port",port, "est fermé")
        f.write("Port "+str (port)+ " => fermé \n")

    finally:
        connexion_principale.close()

def scan_range_ports(start_port, end_port, ip, protocol,f):
    # Fonction pour scanner une plage de ports
    for port in range(start_port, end_port + 1):
        scan_port(port, ip, protocol,f) # Appel de la fonction de scan de port pour chaque port dans la plage
    

# Fonction pour scanner une plage de ports
def scan_range_ports_threads(start_port,end_port, ip, protocol,f):
    threads = [] # Liste pour stocker les threads

    nb_ports = end_port - start_port + 1 # Nombre de ports à scanner
    print(f'Nombre de ports à scanner : {nb_ports}')

    nb_threads = nb_ports // 256 if nb_ports % 256 == 0 else (nb_ports // 256) + 1 # Nombre de threads à créer


    start_thread_port = start_port
    # Création d'un thread pour chaque port dans la plage
    while start_thread_port <= end_port:
        end_thread_port = start_thread_port + 255 # Port de fin pour le thread

        print("Scan du port ", start_thread_port , "au port ", end_thread_port)
        t = threading.Thread(target=scan_range_ports, args=(start_thread_port, end_thread_port, ip, protocol,f))
    
        # Démarrage du thread
        threads.append(t) # Ajout du thread à la liste
        t.start()
        start_thread_port = end_thread_port + 1 # Mise à jour du port de début pour le prochain thread

    for t in threads:
        # Attendre que tous les threads se terminent
        t.join()

# Fonction pour afficher le temps d'exécution
def execution_time(start, end,f):
    # Affichage du temps d'execution
    print("Le Scan de ports a duré :",end-start,"secondes") 
    # Ecriture du temps d'execution dans le fichier de logs
    f.write("===> Le Scan de ports a duré : " + str(end-start)+" secondes\n")

# Affichage du menu
def scanPortMenu() :
    print('=====================Scanneur de Port=====================')

    print_menu()
    
    choix = input('Entrez votre choix : ') 
    
    while choix != '0':
    
        # Ouverture du fichier de logs d'exécution
        f=open ('scan.txt','a',encoding="utf-8")
        
        if choix == '1':
        
            # Choix du port
            port = choose_port()
    
            # Choix de l'adresse IP
            ip = choose_ip()
    
            # Choix du protocole de transport
            protocol = choose_transport_protocol()
    
            # Affichage de l'en-tête de scan
            print(f'Scannage du port {port} sur l\'IP {ip} en {"TCP" if protocol == socket.SOCK_STREAM else "UDP"}...')
            print_header_scanning(f,protocol,ip,str(port))
    
            # Démarrage du chronomètre
            start = time.time() 
    
            # Appel de la fonction de scan de port ici
            scan_port(port, ip, protocol,f)
    
            # Arrêt du chronomètre
            end = time.time()
    
            # Calcul et Affichage du temps d'exécution
            execution_time(start, end,f)
    
        elif choix == '2':
        
            # Choix de la plage de ports
            port_range = choose_range()
    
            # Choix de l'adresse IP
            ip = choose_ip()
    
            # Choix du protocole de transport
            protocol = choose_transport_protocol()
    
            # Affichage de l'en-tête de scan
            print(f'Scannage des ports {port_range[0]}-{port_range[1]}. sur l\' IP {ip} en {"TCP" if protocol == socket.SOCK_STREAM else "UDP"}...')
            print_header_scanning(f,protocol,ip,""+str(port_range[0])+"-"+str(port_range[1]))
    
            # Démarrage du chronomètre
            start = time.time()
    
            # Appel de la fonction de scan de plage de ports ici
            scan_range_ports_threads(int(port_range[0]), int(port_range[1]), ip, protocol,f)
    
            # Arrêt du chronomètre
            end = time.time()
    
            # Calcul et Affichage du temps d'exécution
            execution_time(start, end,f)
    
        elif choix == '3':
        
            ip = choose_ip()
            protocol = choose_transport_protocol()
    
            print(f'Scannage de tous les ports sur l\'IP {ip} en {"TCP" if protocol == socket.SOCK_STREAM else "UDP"}...')
            print_header_scanning(f,protocol,ip,"1-65535")
    
            # Démarrage du chronomètre
            start = time.time()
    
            # Appel de la fonction de scan de plage de ports avec comme paramètres 1 & 65535 pour scanner tous les ports.
            scan_range_ports_threads(1, 65535, ip, protocol,f)
    
            # Arrêt du chronomètre
            end = time.time()
    
            # Calcul et Affichage du temps d'exécution
            execution_time(start, end,f)
        else:
            print('Choix Invalide. Veuillez réessayer.')
    
        # Fermeture du fichier de logs d'exécution
        f.close()
    
        print_menu()
        choix = input('Entrez votre choix: ')