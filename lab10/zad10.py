import time
import math
import multiprocessing

def pierwsza_baza(k):
    for i in range (2,k-1):
        if i*i>k:
            return True
        if k%i == 0:
            return False
    return True


def czy_pierwsza_z_mlp(k,mlp):
    for p in mlp:
        if k%p == 0:
            return False
        if p*p>k:
            return True
    return True

def przygotuj_mlp(max_r):
    s = math.ceil(math.sqrt(max_r))
    mlp = [i for i in range(2, s+1) if pierwsza_baza(i)]
    return mlp


def znajdz_blizniacze_sekwencyjnie(l, r, mlp):
    wynik = []
    for k in range(l, r - 1):
        if czy_pierwsza_z_mlp(k, mlp) and czy_pierwsza_z_mlp(k + 2, mlp):
            wynik.append((k, k + 2))
    return wynik


def worker_blizniacze(args):
    start, end, mlp = args
    lokalne_wyniki = []

    for k in range(start, end):
        if czy_pierwsza_z_mlp(k, mlp):
            if czy_pierwsza_z_mlp(k + 2, mlp):
                lokalne_wyniki.append((k, k + 2))
    return lokalne_wyniki


def znajdz_blizniacze_rownolegle(l, r, mlp, liczba_procesow=None):
    if liczba_procesow is None:
        liczba_procesow = multiprocessing.cpu_count()

    dlugosc_zakresu = (r - 1) - l
    if dlugosc_zakresu <= 0: return []

    liczba_kawalkow = liczba_procesow * 4
    krok = math.ceil(dlugosc_zakresu / liczba_kawalkow)

    zadania = []
    aktualny_start = l

    for _ in range(liczba_kawalkow):
        koniec = min(aktualny_start + krok, r - 1)
        if aktualny_start >= koniec:
            break
        zadania.append((aktualny_start, koniec, mlp))
        aktualny_start = koniec

    with multiprocessing.Pool(processes=liczba_procesow) as pool:
        wyniki_kawalkowe = pool.map(worker_blizniacze, zadania)

    wynik_koncowy = [para for podlista in wyniki_kawalkowe for para in podlista]
    return wynik_koncowy

if __name__ == '__main__':
    L = 1_000_000
    R = 20_000_000

    print(f"Szukanie liczb bliźniaczych w zakresie <{L}, {R}>")
    print(f"Liczba procesorów logicznych: {multiprocessing.cpu_count()}")
    print("-" * 60)

    t_start = time.time()
    mlp = przygotuj_mlp(R)
    print(f"Wygenerowano {len(mlp)} małych liczb pierwszych w {time.time() - t_start:.4f} s.")
    print("-" * 60)

    print("Rozpoczynanie obliczeń SEKWENCYJNYCH...")
    t_seq_start = time.time()
    wynik_seq = znajdz_blizniacze_sekwencyjnie(L, R, mlp)
    t_seq_end = time.time()
    czas_seq = t_seq_end - t_seq_start
    print(f"Czas sekwencyjny: {czas_seq:.4f} s")
    print(f"Znaleziono par: {len(wynik_seq)}")

    print("-" * 60)

    print("Rozpoczynanie obliczeń RÓWNOLEGŁYCH...")
    t_par_start = time.time()
    wynik_par = znajdz_blizniacze_rownolegle(L, R, mlp)
    t_par_end = time.time()
    czas_par = t_par_end - t_par_start

    print(f"Czas równoległy:  {czas_par:.4f} s")
    print(f"Znaleziono par: {len(wynik_par)}")

    zgodnosc = sorted(wynik_seq) == sorted(wynik_par)
    print(f"Weryfikacja wyników: {'ZGODNE' if zgodnosc else 'BŁĄD'}")

    print("-" * 60)

    if czas_par > 0:
        speedup = czas_seq / czas_par
        print(f"Przyspieszenie: {speedup:.2f}x")
    else:
        print("Czas równoległy zbyt krótki na pomiar przyspieszenia.")