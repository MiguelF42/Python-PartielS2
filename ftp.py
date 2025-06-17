from ftplib import FTP
from tools import parserArgs, log
import os


# def printMenu() :
#     print('')
#     print('')
#     print('==============Gestion FTP==============')
#     print('1. Lister les fichiers')
#     print('2. Télécharger un fichier')
#     print('3. Envoyer un fichier')
#     print('4. Supprimer un fichier')
#     print('0. Quitter')

def remove_items(test_list, item):

    # using list comprehension to perform the task
    res = [i for i in test_list if i != item]
    return res

# Define the FTP connection function
def ftpConnexion(ftp_user, ftp_pass) :
    ftp_host = '127.0.0.1'

    try: 
        connexion = FTP(ftp_host)
        connexion.login(ftp_user, ftp_pass)
        return connexion
    except Exception as e:
        print('Erreur de connexion : ', e)
        return None


# Define the FTP commands
## ls command
def ftpLs(connexion, cmd, wd):
    args = parserArgs(cmd)
    target = args[1] if len(args) > 1 else '.'
    try:
        connexion.dir(target)
    except Exception as e:
        print(e)
        print('Le répertoire',target,'n\'existe pas')


## cd command
def ftpCd(connexion, cmd, wd, verbose=True):
    args = parserArgs(cmd)
    target = args[1] if len(args) > 1 else wd
    try:
        connexion.cwd(target)
        wd = connexion.pwd()
    except Exception as e:
        if verbose :
            print('Le répertoire',target,'n\'existe pas')
    return wd


## rename command
def ftpRn(connexion, cmd, wd):
    args = parserArgs(cmd)
    if len(args) < 3 :
        print('Veuillez spécifier un répertoire.')
        return
    target = args[1]
    new_name = args[2]
    try:
        connexion.rename(target, new_name)
    except Exception as e:
        print('Le répertoire',target,'n\'existe pas')


## rm command
def ftpRm(connexion, cmd, wd):
    args = parserArgs(cmd)
    if len(args) < 2 :
        print('Veuillez spécifier un répertoire.')
        return
    target = args[1]
    try:
        connexion.delete(target)
    except Exception as e:
        print('Le fichier',target,'n\'existe pas')


## mkdir command
def ftpMkdir(connexion, cmd, wd):
    args = parserArgs(cmd)
    if len(args) < 2 :
        print('Veuillez spécifier un répertoire.')
        return
    target = args[1]
    try:
        connexion.mkd(target)
    except Exception as e:
        print('Le répertoire',target,'n\'existe pas')


## rmdir command
def ftpRmdir(connexion, cmd, wd):
    args = parserArgs(cmd)
    if len(args) < 2 :
        print('Veuillez spécifier un répertoire.')
        return
    target = args[1]
    try:
        connexion.rmd(target)
    except Exception as e:
        print('Le répertoire',target,'n\'existe pas')


## get command
def ftpGet(connexion, cmd, wd):
    args = parserArgs(cmd)
    if len(args) < 2 :
        print('Veuillez spécifier un fichier.')
        return
    if len(args) < 3 :
        print('Veuillez spécifier un répertoire de destination.')
        return
    target = args[1]
    dest = args[2]
    name = target.split('/')[-1]
    try:
        with open(dest+'/'+name, 'wb') as f:
            connexion.retrbinary('RETR ' + target, f.write)
    except Exception as e:
        print('Le fichier',target,'n\'existe pas :',e)

## send command
def ftpSend(connexion, cmd, wd):
    args = parserArgs(cmd)
    if len(args) < 3 :
        print('Veuillez spécifier un répertoire.')
        return
    target = args[1]
    dest = args[2]
    name = target.split('/')[-1]
    try:
        f = open(target, 'rb')
        connexion.storbinary('STOR '+dest+'/'+name, f)
    except Exception as e:
        print('Le fichier',target,'n\'existe pas :',e)

def ftpCp(connexion, cmd, wd):
    args = parserArgs(cmd)
    if len(args) < 3 :
        print('Veuillez spécifier un répertoire.')
        return
    
    target = args[1]
    new_name = args[2]

    connexion.set_pasv(False)
    connexion.sendcmd('PASV 0')
    sock = connexion.transfercmd('LIST '+target)
    data = sock.recv(1024).decode()
    sock.close()

    lines = data.split('\r\n')

    for line in lines:
        if line == '':
            continue
        data = remove_items(line.split(' '),'')
        name = data[8]
        nameLocal = name.split('/')[-1]

        if len(lines) == 1 and target != name:
            name = target.split('/')[0]+'/'+name

        if data[0].startswith('-'):
            ftpGet(connexion, 'get '+name+' ./temp/', wd)
            ftpSend(connexion, 'send ./temp/'+nameLocal+' '+new_name, wd)
            os.remove('./temp/'+nameLocal)
        elif data[0].startswith('d'):
            ftpCd(connexion, 'cd '+new_name, wd)
            if name not in connexion.nlst():
                ftpMkdir(connexion,'mkdir '+name,wd)
            if not os.path.exists('./temp/'+name):
                os.mkdir('./temp/'+name)
            ftpCp(connexion, 'mv ../'+target+'/'+name+' ../'+new_name+'/'+name, wd)
            os.rmdir('./temp/'+name)
            ftpCd(connexion, 'cd ..', wd)
        else:
            continue

def ftpMv(connexion, cmd, wd):
    args = parserArgs(cmd)
    if len(args) < 3 :
        print('Veuillez spécifier un répertoire.')
        return
    
    target = args[1]
    new_name = args[2]

    connexion.set_pasv(False)
    connexion.sendcmd('PASV 0')
    sock = connexion.transfercmd('LIST '+target)
    data = sock.recv(1024).decode()
    sock.close()

    lines = data.split('\r\n')

    for line in lines:
        if line == '':
            continue
        data = remove_items(line.split(' '),'')
        name = data[8]
        nameLocal = name.split('/')[-1]

        if len(lines) == 1 and target != name:
            name = target.split('/')[-1]+'/'+name

        if data[0].startswith('-'):
            ftpGet(connexion, 'get '+name+' ./temp/', wd)
            ftpSend(connexion, 'send ./temp/'+nameLocal+' '+new_name, wd)
            os.remove('./temp/'+nameLocal)
            ftpRm(connexion, 'rm '+target+'/'+name, wd)
        elif data[0].startswith('d'):
            ftpCd(connexion, 'cd '+new_name, wd)
            if name not in connexion.nlst():
                ftpMkdir(connexion,'mkdir '+name,wd)
            if not os.path.exists('./temp/'+name):
                os.mkdir('./temp/'+name)
            ftpMv(connexion, 'mv ../'+target+'/'+name+' ../'+new_name+'/'+name, wd)
            os.rmdir('./temp/'+name)
            ftpCd(connexion, 'cd ..', wd)
            ftpRmdir(connexion, 'mv ../'+target+'/'+name, wd)
        else:
            continue

def ftpMenu(connexion=None, ftp_user='paris', ftp_pass='1234'):

    print('')
    print('')

    # ftp_user = 'paris' #input('Nom d\'utilisateur : ')
    # ftp_pass = '1234' #input('Mot de passe : ')

    connexion = connexion if connexion is not None else ftpConnexion(ftp_user, ftp_pass)
    if connexion is None:
        print('Impossible de se connecter au serveur FTP.')
        return
    
    print('Connexion réussie au serveur FTP.')


    # printMenu()
    cmd = ''
    wd = '/'

    print(connexion.getwelcome())

    while cmd != 'exit' :
        prompt = ftp_user + '@ftp:'+wd + '>'
        print('You can use `help` to get a list of commands.')
        cmd = input(prompt)

        log(f'{ftp_user}@ftp:{wd} > {cmd}')

        if cmd.startswith('help') :
            print('Liste des commandes disponibles :')
            print('ls [répertoire] - Lister les fichiers dans le répertoire')
            print('cd [répertoire] - Changer de répertoire')
            print('pwd - Afficher le répertoire courant')
            print('rn [ancien nom] [nouveau nom] - Renommer un fichier ou un répertoire')
            print('cp [source] [destination] - Copier un fichier ou un répertoire')
            print('mv [source] [destination] - Déplacer un fichier ou un répertoire')
            print('mkdir [répertoire] - Créer un nouveau répertoire')
            print('rmdir [répertoire] - Supprimer un répertoire vide')
            print('rm [fichier] - Supprimer un fichier')
            print('get [fichier distant] [répertoire local] - Télécharger un fichier du serveur FTP vers le système local')
            print('send [fichier local] [répertoire distant] - Envoyer un fichier du système local vers le serveur FTP')
            print('exit - Quitter le programme')
        
        elif cmd.startswith('ls') :
            ftpLs(connexion, cmd, wd)

        elif cmd.startswith('cd') :
            wd = ftpCd(connexion, cmd, wd)
            print('Répertoire courant : ', wd)

        elif cmd.startswith('pwd') :
            wd = connexion.pwd()
            print('Répertoire courant : ', wd)

        elif cmd.startswith('rn') :
            ftpRn(connexion, cmd, wd)

        elif cmd.startswith('cp'):
            ftpCp(connexion, cmd, wd)

        elif cmd.startswith('mv'):
            ftpMv(connexion, cmd, wd)

        elif cmd.startswith('mkdir') :
            ftpMkdir(connexion, cmd, wd)

        elif cmd.startswith('rmdir') :
            ftpRmdir(connexion, cmd, wd)

        elif cmd.startswith('rm') :
            ftpRm(connexion, cmd, wd)

        elif cmd.startswith('get') :
            ftpGet(connexion, cmd, wd)

        elif cmd.startswith('send') :
            ftpSend(connexion, cmd, wd)
        
        elif cmd.startswith('exit') :
            print('Déconnexion du serveur FTP.')
            connexion.close()
            continue
        else :
            print('Commande non reconnue : ', cmd)

if __name__ == "__main__":
    ftpMenu()