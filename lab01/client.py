import os
import time

f_path = './dane.txt'
r_path = './wyniki.txt'

def client():
    try:
        x = int(input("Input a whole number: "))
        d_fd = os.open(path=f_path, flags=os.O_RDWR | os.O_CREAT, mode=0o666)
        os.write(d_fd, str(x).encode())
        os.close(d_fd)
        if not os.path.exists(r_path):
            f = os.open(path=r_path, flags=os.O_CREAT, mode=0o666)
            os.close(f)

        last_modified = os.path.getmtime(r_path)
        while True:
            # check if value changed
            current_modified = os.path.getmtime(r_path)
            if current_modified != last_modified:
                r_fd = os.open(path=r_path, flags=os.O_RDONLY, mode=0o666)
                length = os.path.getsize(r_fd)
                result = os.read(r_fd, length).decode()
                os.close(r_fd)
                print("Result: ", result)
                break
            else:
                time.sleep(1)

    except ValueError:
        print("Wrong type of value (int required)")

client()