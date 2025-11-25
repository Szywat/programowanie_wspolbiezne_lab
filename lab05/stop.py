import sysv_ipc
import os

KEY_INPUT_QUEUE = 1234
KEY_OUTPUT_QUEUE = 5678

def kill_server():
    pid = os.getpid()
    print(f"[*] Admin Client (PID: {pid}) uruchomiony.")

    try:
        mq_input = sysv_ipc.MessageQueue(KEY_INPUT_QUEUE)
        mq_output = sysv_ipc.MessageQueue(KEY_OUTPUT_QUEUE)
    except sysv_ipc.ExistentialError:
        print("Błąd: Serwer chyba już nie działa (brak kolejek).")
        return

    print("[!] Wysyłam komendę 'stop' do serwera...")

    mq_input.send("stop".encode(), type=pid)

    print("[-] Oczekiwanie na potwierdzenie zamknięcia...")

    try:
        # Odbiór
        response, _ = mq_output.receive(type=pid)
        print(f"[<] Odpowiedź serwera: {response.decode()}")
        print("[*] Operacja zakończona sukcesem. Kolejki powinny zniknąć.")
    except sysv_ipc.ExistentialError:
        # Dla przypadku, w którym serwer usunie kolejkę zanim zdąży odebrać wiadomość
        print("Serwer zamknął kolejkę.")


if __name__ == "__main__":
    kill_server()