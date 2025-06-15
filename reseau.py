import socket
import os
import subprocess
import threading
import re

def print_menu():
    print('')
    print('1. Trouver l\'adresse IP d\'un nom d\'hôte')
    print('2. Trouver le nom d\'hôte à partir d\'une adresse IP')
    print('3. Pinger un hôte')
    print('4. Pinger un réseau (CIDR)')
    print('0. Quitter')


def getIpByHostname(hostname):
    """Get the IP address for a given hostname."""
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror:
        return None

def getHostnameByIp(ip_address):
    """Get the hostname for a given IP address."""
    try:
        hostname = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return None
    
def pingHost(ip):

    command = ["ping", "-c", "1", ip] if os.sys.platform.lower() != "win32" else ["ping", "-n", "1", ip]

    if subprocess.call(command,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL) == 0:
        print(ip + " est joignable")
    else:
        print(ip + " n'est pas joignable")


def binarymask(subnet_mask):
    c = subnet_mask
    mask = []
    for i in range(32) :
        if c > 0:
            mask.append(1)
            c -= 1
        else:
            mask.append(0)
    return mask

def int_to_bin(x):
    if x < 0 or x > 255:
        raise ValueError("Input must be in the range 0-255")
    if x == 0: return [0, 0, 0, 0, 0, 0, 0, 0]
    bit = []
    while x:
        bit.append(x % 2)
        x >>= 1
    bit += [0] * (8 - len(bit))  # Pad to 8 bits
    return bit[::-1]

def bin_to_int(binary):
    if len(binary) != 8:
        raise ValueError("Input must be a list of 8 bits")
    value=0
    for i in range(8):
        if binary[i] == 1:
            value += 2 ** (7 - i)
    return value

def pingNetwork(cidr):
    ipv4_pattern = "(([1-9]{0,1}[0-9]{0,2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]{0,1}[0-9]{0,2}|2[0-4][0-9]|25[0-5])\/([1-2][0-9]|3[0-1])"

    if not re.match(ipv4_pattern, cidr):
        print("Le réseau n'est pas au format CIDR")
        return
    network = cidr.split('/')
    base_ip = network[0]
    binary_mask = binarymask(int(network[1]))

    octets = base_ip.split('.')
    binary_ip = []
    binary_broadcast = []
    c = 0

    for octet in octets:
        binary_octet = int_to_bin(int(octet))
        for i in range(8):
            if binary_mask[c] == 1:
                binary_ip.append(binary_octet[i])
                binary_broadcast.append(binary_octet[i])
            else:
                binary_ip += [0] * (32 - len(binary_ip))
                binary_broadcast += [1] * (32 - len(binary_broadcast))
                break
            c += 1
        if len(binary_ip) == 32:
            break
        

    ipNet = [
        bin_to_int(binary_ip[0:8]),
        bin_to_int(binary_ip[8:16]),
        bin_to_int(binary_ip[16:24]),
        bin_to_int(binary_ip[24:32])
    ]
    ipBroadcast = [
        bin_to_int(binary_broadcast[0:8]),
        bin_to_int(binary_broadcast[8:16]),
        bin_to_int(binary_broadcast[16:24]),
        bin_to_int(binary_broadcast[24:32])
    ]

    incrementeur = []
    # plage = []

    for i in range(4):
        incrementeur.append(ipBroadcast[i] - ipNet[i])

    print(f"Adresse réseau : {ipNet[0]}.{ipNet[1]}.{ipNet[2]}.{ipNet[3]}")
    print(f"Adresse de broadcast : {ipBroadcast[0]}.{ipBroadcast[1]}.{ipBroadcast[2]}.{ipBroadcast[3]}")

    threads = []

    for i in range(incrementeur[0] + 1):
        for j in range(incrementeur[1] + 1):
            for k in range(incrementeur[2] + 1):
                for l in range(incrementeur[3] + 1):
                    ip = f"{ipNet[0] + i}.{ipNet[1] + j}.{ipNet[2] + k}.{ipNet[3] + l}"
                    t = threading.Thread(target=pingHost, args=(ip,))
                    if len(threads) < 255 :
                        # Si le nombre de threads est inférieur à 65536, on ajoute le thread à la liste
                        threads.append(t)

                    else:
                        # Si le nombre de threads est supérieur à 65536, on attend que le premier thread se termine
                        threads[0].join()
                        # On supprime le premier thread de la liste
                        del threads[0]
                        # On ajoute le nouveau thread à la liste
                        threads.append(t)
                    # Démarrage du thread
                    t.start()

    for t in threads:
        # Attendre que tous les threads se terminent
        t.join()

def scanReseauMenu() :
    print('=====================Scanneur Réseau=====================')

    print_menu()

    choix = input("Entrez votre choix : ")

    while choix != "0":

        if choix == "0":
            continue

        elif choix == "1":
            hostname = input("Entrez le nom d'hôte : ")
            ip = getIpByHostname(hostname)
            if ip:
                print(f"L'adresse IP de {hostname} est {ip}")
            else:
                print(f"Impossible de trouver l'adresse IP pour {hostname}")

        elif choix == "2":
            ip_address = input("Entrez l'adresse IP : ")
            hostname = getHostnameByIp(ip_address)
            if hostname:
                print(f"Le nom d'hôte pour {ip_address} est {hostname[0]}")
            else:
                print(f"Impossible de trouver le nom d'hôte pour {ip_address}")

        elif choix == "3":
            ip = input("Entrez l'adresse IP à pinger : ")
            pingHost(ip)

        elif choix == "4":
            cidr = input("Entrez le réseau au format CIDR : ")
            pingNetwork(cidr)

        else:
            print("Choix invalide. Veuillez réessayer.")

        print_menu()
        choix = input('Entrez votre choix: ')