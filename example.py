import sys, socket
#------------------------------------------------
def Name_Host(nomMachine):
    # L'équivalent résolution DNS
    # nomMachine ou URL --> adresse IP
    print("====>   Résolution DNS Nom/URL ==> IP")
    try:
        ip=socket.gethostbyname(nomMachine)  ### Récupérer l'adresse IP d'une machine de nom/URL connu, sinon erreur
        print("L'adresse IP de la machine:",nomMachine,"est :",ip)
         
    except socket.error:
        print("Problème de connexion...")        ### pour le nom ou l'URL inexistant   
        return
    print("====>   Résolution IP ==> Nom/URL")
    ## Résolution inverse : adresse IP --> nomMachine
    try:
        nom=socket.gethostbyaddr(ip)  ### Récupérer le nom/URL d'une machine d'adresse IP connue
        print("nom machine",nom)         
        #print("Le nom de la machine d'adresse IP 192.168.32.90. est:",nom[0]) ## ma GW
        print("Le nom de la machine d'adresse IP:",ip, "est:", nom[0])
        print("Tous les paramètres de la machine :", nom)
         
    except socket.error:
        print ("Erreur socket...")

# ----Programme principal : main

#  Liste de noms/URL d'hôtes
HOTES=["localhost","LAPTOP-7AFCTM82","google.fr", "ESGI.fr","EGSI.fr","URLinéxistant", ""]

# adresses IP des machines de HOTES
for nom in range(len(HOTES)):
    Name_Host(HOTES[nom])

### Autres exemples en IPV6
nom1=socket.gethostbyaddr("2a02:8429:1597:ab01:6518:dea9:bd2b:8e66")
nom2=socket.gethostbyaddr("fe80::7e3c:7788:324b:d104%25")
                          ####2a04:cec0:f045:acc8:e0d9:faf7:6799:7114")
                          ### 192.168.28.59, GW : 192.168.28.225
print("Cas IPV6 PC1",nom1,"\n")
print("Cas IPV6 PC2",nom2)
 
nom3=socket.gethostname()
#("LAPTOP-7AFCTM82")
print("Autre instruction :",nom3)

# fin scan réseau

sys.exit()