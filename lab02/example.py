import os
import time
import errno

# tworzenie pliku zamkowego
while True:
    try:
        #Open file exclusively
        fd = os.open("plikZamkowy", os.O_CREAT|os.O_EXCL|os.O_RDWR)
        break;
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        time.sleep(0.05)
print("plik zamkowy utworzony")

# operacje zabezpieczone plikiem zamkowym
print("operacje zabezpieczone plikiem zamkowym")
time.sleep(2)

# usuwanie pliku zamkowego
os.close(fd)
os.unlink("plikZamkowy")
print("koniec, plik zamkowy zlikwidowany")
