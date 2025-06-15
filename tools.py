import os
import datetime

# Define the function to parse command line arguments
def parserArgs(cmd):
    args = cmd.split(' ')
    return args

logfile = False

def log(message, notime=False):
    global logfile
    if not logfile :
        if not os.path.exists('logs'):
            os.mkdir('logs')
        logfile = f'logs/{datetime.datetime.now().strftime('%Y-%m-%d')}.log'
    with open(logfile, 'a') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f'[{timestamp}] {message} \n' if not notime else f'{message} \n'
        f.write(message)
