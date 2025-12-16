import threading
import time

# tworzenie tablicy liczb
def makeBigArr():
    size = 10_000_000
    return list(range(1, size + 1))

# zapisywanie wyniku wątku pod danym indeksem tablicy
def sumThread(data_part, index, results):
    partial_sum = sum(data_part)
    results[index] = partial_sum

def main():
    thread_count = int(input("Podaj ilość wątków: "))

    print("Generowanie listy...")
    big_arr = makeBigArr()
    total_len = len(big_arr)

    # tworzenie tylu miejsc w tablicy ile jest wątków
    results = [0] * thread_count
    threads = []

    # dzielenie tablicy na kawałki i uruchamianie wątków
    print("Uruchamianie obliczeń...")
    start_time = time.time()

    # obliczanie wielkości kawałka dla wątku
    chunk_size = total_len // thread_count

    for i in range(thread_count):
        # wyznaczanie indeksów start i end dla kawałka
        start_index = i * chunk_size

        # dla pewności bierzemy do rozmiar listy do końca, gdyby się nierówno dzieliło
        if i == thread_count - 1:
            end_index = total_len
        else:
            end_index = (i + 1) * chunk_size

        # wycinanie fragmentu listy dla danego wątku
        sub_list = big_arr[start_index:end_index]

        # tworzenie wątku i dodanie do listy wątków
        t = threading.Thread(target=sumThread, args=(sub_list, i, results))
        threads.append(t)
        t.start()

    # oczekiwanie na zakończenie wszystkich wątków
    for t in threads:
        t.join()

    # sumowanie wyników częściowych
    total_sum = sum(results)
    end_time = time.time()

    print("-" * 30)
    print(f"Wyniki częściowe wątków: {results}")
    print(f"SUMA CAŁKOWITA: {total_sum}")
    print(f"Czas wykonania: {end_time - start_time:.4f} s")

    # weryfikacja
    expected = (1 + total_len) * total_len // 2
    print(f"Weryfikacja:    {expected}")
    print(f"Poprawność:     {'OK' if total_sum == expected else 'BŁĄD'}")

if __name__ == "__main__":
    main()