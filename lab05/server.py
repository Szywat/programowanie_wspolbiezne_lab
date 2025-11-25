import sysv_ipc
import time
import signal
import sys

# Konfiguracja
KEY_INPUT_QUEUE = 1234
KEY_OUTPUT_QUEUE = 5678

POL_ENG = {
    "foka": "seal",
    "kot": "cat",
    "pies": "dog",
    "auto": "car",
    "woda": "water",
    "szkoła": "school",
    "stop": "System shutting down..."
}

def signal_handler(sig, frame):
    print("\n[!] Otrzymano sygnał przerwania (Ctrl+C). Kończenie pracy...")
    raise KeyboardInterrupt


def run_server():
    signal.signal(signal.SIGINT, signal_handler)

    mq_input = None
    mq_output = None

    try:
        # Tworzenie kolejek
        mq_input = sysv_ipc.MessageQueue(KEY_INPUT_QUEUE, sysv_ipc.IPC_CREAT)
        mq_output = sysv_ipc.MessageQueue(KEY_OUTPUT_QUEUE, sysv_ipc.IPC_CREAT)

        print(f"[*] Serwer uruchomiony (PID: {sys.argv[0]}).")
        print(f"[*] Wyślij słowo 'stop' aby bezpiecznie zamknąć serwer.")

        running = True
        while running:
            # Odbiór wiadomości
            message, m_type = mq_input.receive(type=0)

            word = message.decode().strip().lower()
            client_pid = m_type

            print(f"[+] Odebrano od PID {client_pid}: '{word}'")

            # Stop
            if word == "stop":
                print("[!] Otrzymano komendę STOP. Rozpoczynam procedurę zamknięcia.")
                response = "SERWER: Zrozumiałem. Zamykam system i usuwam kolejki."
                running = False  # Wyjście z pętli
            else:
                # Normalna logika słownika + opóźnienie
                print("... przetwarzanie (symulacja obciążenia 2s) ...")
                time.sleep(2)

                if word in POL_ENG:
                    response = POL_ENG[word]
                else:
                    response = "Nie znam takiego słowa"

            # Wysyłanie odpowiedzi
            mq_output.send(response.encode(), type=client_pid)
            print(f"[->] Wysłano odpowiedź do PID {client_pid}")

    except sysv_ipc.ExistentialError:
        print("Błąd: Kolejki już istnieją lub brak uprawnień.")
    except KeyboardInterrupt:
        print("\nPrzerwano działanie serwera.")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")
    finally:
        print("\n[!!!] Sprzątanie systemu IPC...")
        if mq_input:
            mq_input.remove()
            print(f" - Usunięto kolejkę wejściową ({KEY_INPUT_QUEUE})")
        if mq_output:
            mq_output.remove()
            print(f" - Usunięto kolejkę wyjściową ({KEY_OUTPUT_QUEUE})")
        print("[*] Serwer zakończył pracę bezpiecznie.")


if __name__ == "__main__":
    run_server()