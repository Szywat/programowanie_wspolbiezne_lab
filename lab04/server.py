import os
import struct
import signal
import time
import sys

SERVER_FIFO = "/tmp/server_fifo"
DB = {
    1: "FOKA",
    2: "KOT",
    3: "PIES"
}
MAX_NAME_LEN = 20
RESPONSE_DELAY = 2

server_fd = None

def signal_handler(sig, frame):
    global server_fd
    if sig == signal.SIGUSR1:
        print(f"\n[ROOT] Received SIGUSR1 – closing server...")
        if server_fd is not None:
            try:
                os.close(server_fd)
            except:
                pass
        if os.path.exists(SERVER_FIFO):
            os.unlink(SERVER_FIFO)
        sys.exit(0)
    else:
        print(f"[ROOT] Ignored signal: {signal.strsignal(sig)}")


signal.signal(signal.SIGHUP, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGUSR1, signal_handler)

if os.path.exists(SERVER_FIFO):
    os.unlink(SERVER_FIFO)
os.mkfifo(SERVER_FIFO)
print(f"[ROOT] Listening to {SERVER_FIFO}")

try:
    server_fd = os.open(SERVER_FIFO, os.O_RDONLY)
    print("[ROOT] Input queue opened (blocking read)")

    while True:
        data = os.read(server_fd, 4)
        if not data:
            continue

        msg_len = struct.unpack('!i', data)[0]
        if msg_len <= 0:
            continue

        rest = b''
        while len(rest) < msg_len:
            chunk = os.read(server_fd, msg_len - len(rest))
            if not chunk:
                break
            rest += chunk

        if len(rest) < msg_len:
            continue

        id_val = struct.unpack('!i', rest[:4])[0]
        client_fifo = rest[4:].decode('utf-8').rstrip('\x00')

        print(f"[ROOT] Request: ID={id_val}, client: {client_fifo}")

        if id_val in DB:
            name = DB[id_val]
        else:
            name = "No data found"

        name_bytes = name.encode('utf-8')
        if len(name_bytes) > MAX_NAME_LEN:
            name_bytes = name_bytes[:MAX_NAME_LEN]

        resp_len = len(name_bytes)
        header = struct.pack('!i', resp_len)

        response = header + name_bytes
        try:
            client_fd = os.open(client_fifo, os.O_WRONLY)
            os.write(client_fd, response)
            os.close(client_fd)
            print(f"[ROOT] Response sent: '{name}'")
        except Exception as e:
            print(f"[ROOT] Response Error: {e}")

        time.sleep(RESPONSE_DELAY)

except KeyboardInterrupt:
    print("\n[ROOT] Keyboard interrupt received – closing server...")
finally:
    if server_fd is not None:
        try:
            os.close(server_fd)
        except:
            pass
    if os.path.exists(SERVER_FIFO):
        os.unlink(SERVER_FIFO)
    print("[ROOT] Closed.")