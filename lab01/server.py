import os
import time
f_path = './dane.txt'
r_path = './wyniki.txt'

def detect_file_change(file_path, interval=1):
    if not os.path.exists(file_path):
        f = os.open(path=file_path, flags= os.O_CREAT, mode=0o666)
        os.close(f)

    last_modified = os.path.getmtime(file_path)
    while True:
        current_modified = os.path.getmtime(file_path)
        if current_modified != last_modified:
            fd = os.open(path=file_path, flags=os.O_RDONLY, mode=0o666)
            fd_length = os.path.getsize(file_path)
            number = os.read(fd, fd_length).decode()
            if len(number) == 0:
                print("Plik 'dane.txt' jest pusty!")
            else:
                calculated_number = calculate(int(number))
                save_result(r_path, calculated_number)
                last_modified = current_modified
                os.close(fd)
        time.sleep(interval)


def calculate(x):
    return x**2 + x - 1

def save_result(result_path, result):
    fd = os.open(path=result_path, flags=os.O_RDWR | os.O_CREAT, mode=0o666)
    os.write(fd, str(result).encode())
    os.close(fd)

detect_file_change('dane.txt')