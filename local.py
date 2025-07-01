import os
from tools import parserArgs,log
from ftplib import FTP
from ftp import ftpSend, ftpGet
import shutil

def localLs(cmd, wd): # Lister le contenu d'un répertoire local
    args = parserArgs(cmd)
    target = args[1] if len(args) > 1 else wd
    try:
        print('\n'.join(os.listdir(target)))
    except Exception as e:
        print('Le répertoire',target,'n\'existe pas : ')

def localCd(cmd, wd): # Changer de répertoire local
    args = parserArgs(cmd)
    if len(args) < 2: # Vérifie si un répertoire a été spécifié
        print('Veuillez spécifier un répertoire.')
        return wd
    target = args[1]
    new_wd = os.path.join(wd, target) if not os.path.isabs(target) else target # Chemin absolu ou relatif
    if os.path.isdir(new_wd):
        if target == '..' or target == '../':
            folders = wd.split('/')
            folders.pop(len(folders) - 1)
            new_wd = '/'.join(folders) if folders else '/' # Si on est à la racine, on reste à la racine
        elif target == '.' or target == './':
            return wd

        return new_wd
    else:
        print('Le répertoire', target, 'n\'existe pas')
        return wd
    
def localMkdir(cmd, wd): # Créer un répertoire local
    args = parserArgs(cmd)
    if len(args) < 2: # Vérifie si un nom de répertoire a été spécifié
        print('Veuillez spécifier un répertoire.')
        return
    target = args[1]
    new_dir = os.path.join(wd, target) if not os.path.isabs(target) else target # Chemin absolu ou relatif
    try:
        os.makedirs(new_dir) # Crée tous les répertoires intermédiaires nécessaires
        print('Répertoire créé :', new_dir)
    except Exception as e:
        print('Erreur lors de la création du répertoire :', e)

def localRmdir(cmd, wd): # Supprimer un répertoire local
    args = parserArgs(cmd)
    if len(args) < 2: # Vérifie si un répertoire a été spécifié
        print('Veuillez spécifier un répertoire.')
        return

    y=input('Êtes-vous sûr de vouloir supprimer le répertoire ? (y/n) ')
    if y.lower() != 'y':
        print('Suppression annulée.')
        return

    target = args[1]
    dir_to_remove = os.path.join(wd, target) if not os.path.isabs(target) else target # Chemin absolu ou relatif
    try:
        os.rmdir(dir_to_remove) # Supprime le répertoire s'il est vide
        print('Répertoire supprimé :', dir_to_remove)
    except Exception as e:
        print('Erreur lors de la suppression du répertoire :', e)

def localRn(cmd, wd): # Renommer un fichier local
    args = parserArgs(cmd)
    if len(args) < 3: # Vérifie si un fichier et un nouveau nom ont été spécifiés
        print('Veuillez spécifier un fichier et un nouveau nom.')
        return
    target = args[1]
    new_name = args[2]
    file_to_rename = os.path.join(wd, target) if not os.path.isabs(target) else target # Chemin absolu ou relatif du fichier à renommer
    new_file_name = os.path.join(wd, new_name) if not os.path.isabs(new_name) else new_name # Chemin absolu ou relatif du nouveau nom
    if not os.path.exists(file_to_rename):
        print('Le fichier', target, 'n\'existe pas')
        return
    try:
        os.rename(file_to_rename, new_file_name)
        print('Fichier renommé de', file_to_rename, 'à', new_file_name)
    except Exception as e:
        print('Erreur lors du renommage du fichier :', e)

def localMv(cmd, wd): # Déplacer un fichier local
    args = parserArgs(cmd)
    if len(args) < 3: # Vérifie si un fichier et un nouveau nom ont été spécifiés
        print('Veuillez spécifier un fichier et un nouveau nom.')
        return
    target = args[1]
    new_name = args[2]
    file_to_move = os.path.join(wd, target) if not os.path.isabs(target) else target # Chemin absolu ou relatif du fichier à déplacer
    new_file_path = os.path.join(wd, new_name) if not os.path.isabs(new_name) else new_name # Chemin absolu ou relatif du nouvel emaplcement
    if not os.path.exists(file_to_move):
        print('Le fichier', target, 'n\'existe pas')
        return
    try:
        os.rename(file_to_move, new_file_path)
        print('Fichier déplacé de', file_to_move, 'à', new_file_path)
    except Exception as e:
        print('Erreur lors du déplacement du fichier :', e)

def localCp(cmd, wd): # Copier un fichier local
    args = parserArgs(cmd)
    if len(args) < 3: # Vérifie si un fichier et un nouveau nom ont été spécifiés
        print('Veuillez spécifier un fichier et un nouveau nom.')
        return
    target = args[1]
    new_name = args[2]
    file_to_move = os.path.join(wd, target) if not os.path.isabs(target) else target # Chemin absolu ou relatif du fichier à copier
    new_file_path = os.path.join(wd, new_name) if not os.path.isabs(new_name) else new_name # Chemin absolu ou relatif de la destination de la copie
    if not os.path.exists(file_to_move):
        print('Le fichier', target, 'n\'existe pas')
        return
    try:
        if os.path.isfile(file_to_move):
            shutil.copy2(file_to_move, new_file_path) # Utilise copy2 pour conserver les métadonnées du fichier
        else:
            shutil.copytree(file_to_move, new_file_path) # Utilise copytree pour copier les répertoires
        print('Fichier copié de', file_to_move, 'à', new_file_path)
    except Exception as e:
        print('Erreur lors de la copie du fichier :', e)


def localRm(cmd, wd): # Supprimer un fichier local
    args = parserArgs(cmd)
    if len(args) < 2: # Vérifie si un fichier a été spécifié
        print('Veuillez spécifier un fichier.')
        return
    
    y=input('Êtes-vous sûr de vouloir supprimer le répertoire ? (y/n) ')
    if y.lower() != 'y':
        print('Suppression annulée.')
        return
    
    force = False

    if len(args) == 3:
        if args[2] == '-f':
            force = True
        else:
            print('Option inconnue :', args[2])
            return
        target = args[2]
    target = args[1]
    file_to_remove = os.path.join(wd, target) if not os.path.isabs(target) else target # Chemin absolu ou relatif du fichier à supprimer
    try:
        shutil.rmtree(file_to_remove) if force else os.remove(file_to_remove) 
        print('Fichier supprimé :', file_to_remove)
    except Exception as e:
        print('Erreur lors de la suppression du fichier :', e)

# def localConnexion(): # Établir une connexion FTP locale
#     ftp_host = '127.0.0.1'

#     try: 
#         connexion = FTP(ftp_host)
#         connexion.login('test', '1234')3
#         return connexion
#     except Exception as e:
#         print('Erreur de connexion : ', e)
#         return None

def localGet(cmd, wd, connexion): # Télécharger un fichier distant
    args = parserArgs(cmd)
    if len(args) < 3:
        print('Veuillez spécifier un fichier distant à télécharger.')
        return
    try:
        ftpGet(connexion, cmd, wd)
    except Exception as e:
        print('Erreur lors du téléchargement du fichier :', e)

def localSend(cmd, wd, connexion): # Envoyer un fichier local
    args = parserArgs(cmd)
    if len(args) < 3:
        print('Veuillez spécifier un fichier local à envoyer.')
        return
    if not os.path.exists(wd+'/'+args[1]):
        print('Le fichier', args[1], 'n\'existe pas')
        return
    
    new_cmd = 'send ' + wd + '/' + args[1] + ' ' + args[2]
    try:
        ftpSend(connexion, new_cmd, wd)
    except Exception as e:
        print('Erreur lors de l\'envoi du fichier :', e)

def localMenu(connexion): # Afficher le menu local
    print('')
    print('')

    # printMenu()
    cmd = ''
    wd = 'C:/' if os.name == 'nt' else '/'
    print('You can use `help` to get a list of commands.')

    while cmd != 'exit' :
        prompt = wd + '>'
        cmd = input(prompt)

        log(f'{wd}>{cmd}')

        if cmd.startswith('help') :
            print('Liste des commandes disponibles :')
            print('ls [répertoire] - Lister le contenu d\'un répertoire')
            print('cd [répertoire] - Changer de répertoire')
            print('pwd - Afficher le répertoire courant')
            print('rn [fichier] [nouveau nom] - Renommer un fichier')
            print('cp [fichier] [nouveau nom] - Copier un fichier (non implémenté)')
            print('mv [fichier] [nouveau nom] - Déplacer un fichier')
            print('mkdir [répertoire] - Créer un répertoire')
            print('rmdir [répertoire] - Supprimer un répertoire')
            print('rm [fichier] - Supprimer un fichier')
            print('get [fichier distant] - Télécharger un fichier (non implémenté)')
            print('send [fichier local] - Envoyer un fichier (non implémenté)')
            print('exit - Quitter le programme')

        elif cmd.startswith('ls') :
            localLs(cmd, wd)

        elif cmd.startswith('cd') :
            wd = localCd(cmd, wd)

        elif cmd.startswith('pwd') :
            print(wd)

        elif cmd.startswith('rn') :
            localRn(cmd, wd)

        elif cmd.startswith('cp') :
            localCp(cmd, wd)
        
        elif cmd.startswith('mv') :
            localMv(cmd, wd)
        
        elif cmd.startswith('mkdir') :
            localMkdir(cmd, wd)

        elif cmd.startswith('rmdir') :
            localRmdir(cmd, wd)

        elif cmd.startswith('rm') :
            localRm(cmd, wd)

        elif cmd.startswith('get') :
            localGet(cmd, wd, connexion)

        elif cmd.startswith('send') :
            localSend(cmd, wd, connexion)
        elif cmd.startswith('exit') :
            continue
        else :
            print('Commande inconnue :', cmd)

if __name__ == "__main__":
    localMenu()