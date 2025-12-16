import socket

IP = "127.0.0.1"
PORT = 5001
BUF_SIZE = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((IP, PORT))

print(f"Serwer gry działa na {IP}:{PORT}")

gracze = []  # lista aktualnych graczy [(ip, port)]
ruchy = {}  # słownik ruchów
punkty = {}  # słownik punktów
poprzedni_gracze = []  # zabezpieczenie przed graczami widmo


def reset_gry():
    global gracze, ruchy, punkty, poprzedni_gracze
    # przed czyszczeniem zapisujemy kto grał, żeby ignorować ich spóźnione pakiety
    poprzedni_gracze = gracze[:]

    gracze = []
    ruchy = {}
    punkty = {}
    print("--- Rozgrywka zakończona. Reset serwera. ---")


def oblicz_wynik(r1, r2):
    if r1 == r2: return 0
    if (r1 == 'p' and r2 == 'k') or (r1 == 'k' and r2 == 'n') or (r1 == 'n' and r2 == 'p'):
        return 1
    return 2


while True:
    try:
        data, addr = server_socket.recvfrom(BUF_SIZE)
        wiadomosc = data.decode().strip().lower()

        # ochrona przed graczem widmo
        # jeśli wiadomość przychodzi od kogoś, kto przed chwilą skończył grę,
        # a lista graczy jest pusta (lub niepełna), ignorujemy to jako "spóźniony pakiet".
        if addr in poprzedni_gracze and addr not in gracze:
            print(f"Zignorowano spóźniony pakiet od poprzedniego gracza: {addr}")
            server_socket.sendto("KONIEC_GRY".encode(), addr)  # Upewniamy się, że klient wie o końcu
            continue

        # obsługa "koniec"
        if wiadomosc == "koniec":
            if addr in gracze:
                print(f"Otrzymano 'koniec' od gracza {addr}")
                # powiadom drugiego gracza
                for g in gracze:
                    if g != addr:
                        server_socket.sendto("KONIEC_GRY".encode(), g)
                reset_gry()
            continue

        # rejestracja nowego gracza
        if addr not in gracze:
            if len(gracze) < 2:
                gracze.append(addr)
                punkty[addr] = 0
                print(f"Dołączył nowy gracz: {addr}. Liczba graczy: {len(gracze)}")

                # jeśli mamy komplet nowych graczy, czyścimy listę poprzednich,
                if len(gracze) == 2:
                    poprzedni_gracze = []
            else:
                server_socket.sendto("SERWER PEŁNY".encode(), addr)
                continue

        # obsługa ruchów
        if wiadomosc in ['p', 'k', 'n']:
            ruchy[addr] = wiadomosc
            print(f"Gracz {addr} wybrał: {wiadomosc}")

            if len(gracze) == 2 and len(ruchy) == 2:
                p1, p2 = gracze[0], gracze[1]
                res = oblicz_wynik(ruchy[p1], ruchy[p2])

                if res == 1:
                    punkty[p1] += 1
                elif res == 2:
                    punkty[p2] += 1

                msg_p1 = f"{'WYGRANA' if res == 1 else 'PRZEGRANA' if res == 2 else 'REMIS'}|{ruchy[p2]}"
                msg_p2 = f"{'WYGRANA' if res == 2 else 'PRZEGRANA' if res == 1 else 'REMIS'}|{ruchy[p1]}"

                server_socket.sendto(msg_p1.encode(), p1)
                server_socket.sendto(msg_p2.encode(), p2)
                ruchy = {}
        else:
            server_socket.sendto("BŁĄD: Nieznana komenda".encode(), addr)

    except Exception as e:
        print(f"Błąd serwera: {e}")