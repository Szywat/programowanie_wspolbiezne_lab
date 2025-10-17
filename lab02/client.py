import os
import time
import sys
bufor_path='./buforSerwera'
client_file='plikKlienta'

def client():
    # os.open()
    lcf = list_client_files('./')
    create_client_files(lcf)
    # print(sys.argv[0])


def list_client_files(path):
    ld = os.listdir(path)
    cf_list = []
    for f in ld:
        if f.startswith('plikKlienta'):
            cf_list.append(f)
    return cf_list

def create_client_files(l):
    if len(l) == 0:
        fd = os.open(f'{client_file}1', os.O_CREAT)
        os.close(fd)
    else:
        nl = []
        for c in l:
            x = c.strip('plikKlienta')
            nl.append(int(x))
        print(nl)

        for i in range(int(max(nl))):
            filename = f'{client_file}{i+1}'
            if os.path.exists(filename):
                print("Istnieje: " + filename)
            else:
                print("Nie istnieje: " + filename)
                fd = os.open(filename, os.O_CREAT)
                os.close(fd)
                break

client()