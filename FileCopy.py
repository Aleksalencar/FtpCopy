import os.path, os
from ftplib import FTP, error_perm
import threading
from tkinter import filedialog

host = '192.168.1.124'
port = 2121

ftp = FTP()
ftp.connect(host, port)
ftp.login('anime', 'anime')


def list_dir():
    files = []

    try:
        files = ftp.nlst()
    except error_perm as resp:
        if str(resp) == "550 No files found":
            print("No files in this directory")
        else:
            raise
    for f in files:
        print(f)


def place_files(ftp, path_file):
    if os.path.isfile(path_file):
        name = path_file.split('/')[-1]
        try:
            print("Armazenando", name)
            resp = ftp.storbinary('STOR ' + name, open(path_file, 'rb'))
            print(resp, ' [', name, ']')
        except:
            print('Falha')

def mkdir(dir_name):
    try:
        ftp.mkd(dir_name)
        print('Criando dir ', dir_name)
        # ignore "directory already exists"
    except error_perm as e:
        if not e.args[0].startswith('550'):
            raise


dir_paths = filedialog.askopenfilenames()
dir_name = dir_paths[0].split('/')[-2]
ftp.cwd('/0/Anime')
mkdir(dir_name)
ftp.cwd(dir_name)
list_dir()
for file in dir_paths:
    place_files(ftp,file)
ftp.quit()
