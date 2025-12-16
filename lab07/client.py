import socket
import sys

SERVER_ADDR = ("127.0.0.1", 5001)
BUF_SIZE = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("--- KLIENT UDP: PAPIER, KAMIEŃ, NOŻYCE ---")
print("Wpisz: 'p', 'k', 'n' lub 'koniec'")

moje_punkty = 0

while True:
    try:
        # pobranie ruchu
        wybor = input("\nTwój wybór: ").strip().lower()

        # walidacja lokalna
        if wybor not in ['p', 'k', 'n', 'koniec']:
            print("Niepoprawny wybór.")
            continue

        # wysyłanie do serwera
        client_socket.sendto(wybor.encode(), SERVER_ADDR)

        if wybor == "koniec":
            print("Zakończyłeś rozgrywkę.")
            break

        print("Oczekiwanie na odpowiedź serwera...")

        # odbiór odpowiedzi
        data, _ = client_socket.recvfrom(BUF_SIZE)
        msg = data.decode()

        if msg == "SERWER_PEŁNY":
            print("\n>>> Serwer pełny. Nie można dołączyć. <<<")
            break

        if msg == "KONIEC_GRY":
            print("\n>>> Drugi gracz opuścił grę. KONIEC. <<<")
            break

        # obsługa wyniku rundy
        if "|" in msg:
            wynik, ruch_opp = msg.split("|")
            mapa = {'p': 'Papier', 'k': 'Kamień', 'n': 'Nożyce'}

            print(f"Przeciwnik: {mapa.get(ruch_opp, ruch_opp)}")
            if wynik == "WYGRANA":
                moje_punkty += 1
                print(">>> WYGRAŁEŚ! <<<")
            elif wynik == "PRZEGRANA":
                print(">>> Przegrałeś. <<<")
            else:
                print(">>> Remis. <<<")

            print(f"Twoje punkty: {moje_punkty}")

    except KeyboardInterrupt:
        # obsługa Ctrl+C
        client_socket.sendto("koniec".encode(), SERVER_ADDR)
        print("\nPrzerwano.")
        break
    except Exception as e:
        print(f"Błąd: {e}")
        break

client_socket.close()