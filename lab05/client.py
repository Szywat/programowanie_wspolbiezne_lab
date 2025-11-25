import sysv_ipc
import os
import time

KEY_INPUT_QUEUE = 1234
KEY_OUTPUT_QUEUE = 5678
NUM_REQUESTS = 10


def run_single_client():
    pid = os.getpid()
    print(f"[*] Klient (PID: {pid}) uruchomiony.")

    try:
        msg = input("Podaj słowo do wysłania: ").strip()
    except EOFError:
        return

    if not msg:
        print("Nie podano słowa. Kończę działanie.")
        return

    try:
        mq_input = sysv_ipc.MessageQueue(KEY_INPUT_QUEUE)
        mq_output = sysv_ipc.MessageQueue(KEY_OUTPUT_QUEUE)
    except sysv_ipc.ExistentialError:
        print("Błąd: Serwer nie działa (nie znaleziono kolejek IPC).")
        return

    for i in range(NUM_REQUESTS):

        try:
            mq_input.send(msg.encode(), type=pid)
            print(f" [PID {pid}] Wysłano zapytanie {i+1}")
            time.sleep(0.5)
        except sysv_ipc.ExistentialError:
            print(" [!] Kolejka zniknęła! Serwer został wyłączony.")
            return


    print("--- Odbieranie ---")
    for i in range(NUM_REQUESTS):
        try:
            response, _ = mq_output.receive(type=pid)
            print(f" [PID {pid}] Odpowiedź: {response.decode()}")
        except sysv_ipc.ExistentialError:
            print(" [!] Błąd: Kolejka zniknęła podczas oczekiwania.")
        except sysv_ipc.BusyError:
            print(" [!] Kolejka zajęta.")


if __name__ == "__main__":
    run_single_client()