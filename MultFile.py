from multiprocessing import Pool, freeze_support
import os.path, os
from ftplib import FTP, error_perm
from tkinter import filedialog

host = '192.168.1.124'
port = 2121


def place_files(ftp, path_file):
    if os.path.isfile(path_file):
        name = path_file.split('/')[-1]
        try:
            print("Armazenando", name)
            resp = ftp.storbinary('STOR ' + name, open(path_file, 'rb'))
            print(resp, '[', name, ']')
        except:
            print('Falha')


def mkdir(ftp, dir_name):
    try:
        ftp.mkd(dir_name)
        print('Criando dir ', dir_name)
        # ignore "directory already exists"
    except error_perm as e:
        if not e.args[0].startswith('550'):
            raise


def new_login():
    ftp = FTP()
    ftp.connect(host, port)
    ftp.login('anime', 'anime')
    return ftp


def upload(file):
    ftp = new_login()
    dir_name = file.split('/')[-2]

    ftp.cwd('/0/Anime')
    mkdir(ftp, dir_name)
    ftp.cwd(dir_name)

    place_files(ftp, file)
    ftp.quit()


if __name__ == '__main__':
    infiles = filedialog.askopenfilenames()
    infiles = infiles

    freeze_support()
    pool = Pool()  # submit 10 at once
    pool.map(upload, infiles)
