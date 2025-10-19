import os
import time
import errno

bd = "./bufor.txt"
ld = "./lockfile"
end = ";"
c_id = os.getpid()
cf = f"client{c_id}.txt"

def client():
    create_lockfile()

    print("Message to the server (end with new line): ")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    message = "\n".join(lines)

    with open(bd, "w") as bufor:
        bufor.write(cf + "\n")
        bufor.write(message + "\n")
        bufor.write(end + "\n")

    print("Message sent!")

    print("Waiting for response...")
    while not os.path.exists(cf):
        time.sleep(1)

    with open(cf, "r") as client_file:
        response = client_file.read().replace(end, "").strip()
        print(f"\nServer's response:\n{response}")
        time.sleep(3)

    os.remove(cf)

def create_lockfile():
    while True:
        try:
            lockfile = os.open(path=ld,
                               flags=os.O_CREAT | os.O_EXCL | os.O_RDWR)
            os.close(lockfile)
            break
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
            print("Server's busy, please wait...")
            time.sleep(5)

client()