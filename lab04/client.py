import os
import struct
import sys
import uuid

SERVER_FIFO = "/tmp/server_fifo"
TMP = "/tmp"


def main():
    wanted_id = input("Search for ID: ")

    try:
        id_val = int(wanted_id)
    except ValueError:
        print("ID must be a whole number!")
        sys.exit(1)

    client_fifo = f"{TMP}/client_{uuid.uuid4().hex[:8]}_fifo"
    os.mkfifo(client_fifo)
    print(f"[CLI] Queue: {client_fifo}")

    try:
        client_path_bytes = client_fifo.encode('utf-8')
        msg_body = struct.pack('!i', id_val) + client_path_bytes + b'\x00'
        msg_len = len(msg_body)
        header = struct.pack('!i', msg_len)
        message = header + msg_body

        server_fd = os.open(SERVER_FIFO, os.O_WRONLY)
        os.write(server_fd, message)
        os.close(server_fd)
        print(f"[CLI] Sent request: ID={id_val}")

        client_fd = os.open(client_fifo, os.O_RDONLY)
        data = os.read(client_fd, 4)
        if not data:
            print("[CLI] No response (server error)")
            return

        resp_len = struct.unpack('!i', data)[0]
        response = b''
        while len(response) < resp_len:
            chunk = os.read(client_fd, resp_len - len(response))
            if not chunk:
                break
            response += chunk

        name = response.decode('utf-8', errors='ignore').rstrip('\x00')
        print(f"[CLI] Response: {name}")

    except Exception as e:
        print(f"[CLI] Error: {e}")
    finally:
        if os.path.exists(client_fifo):
            os.unlink(client_fifo)
        print(f"[CLI] Deleted {client_fifo}")


if __name__ == "__main__":
    main()