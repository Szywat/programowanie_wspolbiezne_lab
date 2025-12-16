import sysv_ipc
import time
import sys

klucz = 1234
CARD_LETTERS = ["A", "B", "C"]


def playerChoice(player_name):
    while True:
        try:
            print(f"[{player_name}] Twój ruch.")
            card = str(input("Wybierz literę karty (A, B lub C): ")).strip().upper()
            if card not in CARD_LETTERS:
                raise ValueError
            return card
        except ValueError:
            print("Błąd: Podano złą wartość. Wpisz A, B lub C.")
        except Exception:
            print("Błąd danych.")


def game_logic(isFirst, sem1, sem2, shm1, shm2):
    my_name = "Gracz 1" if isFirst else "Gracz 2"

    # Gracz 1: shm1, sem1
    # Gracz 2: shm2, sem2
    if isFirst:
        my_shm = shm1
        opp_shm = shm2
        my_sem = sem1
        opp_sem = sem2
    else:
        my_shm = shm2
        opp_shm = shm1
        my_sem = sem2
        opp_sem = sem1

    my_score = 0
    opp_score = 0

    print(f"Jesteś: {my_name}. Rozpoczynam grę (3 tury).")

    for tura in range(1, 4):
        print(f"\n--- TURA {tura} ---")

        choice = playerChoice(my_name) # wybiera litere
        my_shm.write(choice.encode()) # zapisuje litere

        # skończył i czeka
        print("Czekam na ruch przeciwnika...")
        my_sem.release()  # podnosi semafor (0 -> 1)
        opp_sem.acquire()  # czekam aż przeciwnik podniesie swój (1 -> 0)

        # w tym momencie gracze mają zapisane dane w pamięci

        # odczyt i wyniki
        opp_data = opp_shm.read(byte_count=1)
        opp_choice = opp_data.decode().strip('\x00')

        print(f"Twój wybór: {choice} | Wybór przeciwnika: {opp_choice}")

        winner = ""
        if choice == opp_choice:
            winner = "Gracz 2"
            if not isFirst:
                my_score += 1
                print("-> Wygrałeś turę!")
            else:
                opp_score += 1
                print("-> Przegrałeś turę.")
        else:
            winner = "Gracz 1"
            if isFirst:
                my_score += 1
                print("-> Wygrałeś turę!")
            else:
                opp_score += 1
                print("-> Przegrałeś turę.")

        print(
            f"Wynik po turze {tura}: Gracz 1 [{my_score if isFirst else opp_score}] - [{opp_score if isFirst else my_score}] Gracz 2")

        if tura < 3:
            print("Czekam na gotowość przeciwnika do kolejnej tury...")
        else:
            print("Kończenie gry...")

        my_sem.release()  # Sygnalizuję: skończyłem czytać
        opp_sem.acquire()  # Czekam: aż przeciwnik skończy czytać

    print("\nKoniec rozgrywki.")


def main():
    cleanup_needed = False

    try:
        sem1 = sysv_ipc.Semaphore(klucz, sysv_ipc.IPC_CREX, 0o700, 0)
        sem2 = sysv_ipc.Semaphore(klucz + 1, sysv_ipc.IPC_CREX, 0o700, 0)

        sharedMemory1 = sysv_ipc.SharedMemory(klucz, sysv_ipc.IPC_CREX, 0o700, 10)
        sharedMemory2 = sysv_ipc.SharedMemory(klucz + 1, sysv_ipc.IPC_CREX, 0o700, 10)

        pierwszy = True
        cleanup_needed = True  # Tylko twórca sprząta
        print("Utworzono zasoby. Jestem GRACZ 1.")

    except sysv_ipc.ExistentialError: # jeśli już wszystko powstało - dołączamy jako gracz 2
        try:
            time.sleep(0.2)
            sem1 = sysv_ipc.Semaphore(klucz)
            sem2 = sysv_ipc.Semaphore(klucz + 1)
            sharedMemory1 = sysv_ipc.SharedMemory(klucz)
            sharedMemory2 = sysv_ipc.SharedMemory(klucz + 1)

            pierwszy = False
            cleanup_needed = False
            print("Dołączono do gry. Jestem GRACZ 2.")
        except sysv_ipc.ExistentialError:
            print("Błąd: Nie można połączyć się z zasobami.")
            return

    try:
        game_logic(pierwszy, sem1, sem2, sharedMemory1, sharedMemory2)
    except KeyboardInterrupt:
        print("\nPrzerwano grę przez użytkownika.")
    finally:
        # usuwamy zasoby tylko jeśli jesteśmy Graczem 1
        if cleanup_needed:
            print("Usuwanie zasobów IPC...")
            try:
                sem1.remove()
                sem2.remove()
                sharedMemory1.remove()
                sharedMemory2.remove()
                print("Zasoby usunięte.")
            except Exception as e:
                print(f"Błąd podczas usuwania: {e}")


if __name__ == '__main__':
    main()