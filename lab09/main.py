import threading
import time

START=15_000
END=100_000

# tworzenie tablicy liczb
def makeBigArr():
    return list(range(START, END + 1))

def isPrime(k):
    for i in range (2,k-1):
        if i*i>k:
            return True
        if k%i == 0:
            return False
    return True

# zapisywanie wyniku wątku pod danym indeksem tablicy
def getPrimeThread(data_part, index, results, bar):
    # partial_sum = sum(data_part)
    partial_arr= [i for i in data_part if isPrime(i)]
    results[index] = partial_arr
    bar.wait()

def main():
    thread_count = int(input("Podaj ilość wątków: "))
    b = threading.Barrier(thread_count+1)

    print("Generowanie listy...")
    big_arr = makeBigArr()
    total_len = len(big_arr)

    # tworzenie tylu miejsc w tablicy ile jest wątków
    results = [0] * thread_count

    # dzielenie tablicy na kawałki i uruchamianie wątków
    print("Uruchamianie obliczeń...")
    start_time = time.time()

    # obliczanie wielkości kawałka dla wątku
    chunk_size = total_len // thread_count
    for i in range(thread_count):
        print(f"{i+1} przejście")
        # wyznaczanie indeksów start i end dla kawałka
        start_index = i * chunk_size

        # dla pewności bierzemy rozmiar listy do końca, gdyby się nierówno dzieliło
        if i == thread_count - 1:
            end_index = total_len
        else:
            end_index = (i + 1) * chunk_size

        # wycinanie fragmentu listy dla danego wątku
        sub_list = big_arr[start_index:end_index]

        # tworzenie wątku i wystartowanie go
        t = threading.Thread(target=getPrimeThread, args=(sub_list, i, results,b))
        t.start()

    # oczekiwanie na zakończenie wszystkich wątków
    b.wait()
    end_time = time.time()

    print("-" * 30)
    print(f"Wyniki częściowe wątków: {results}")
    print(f"Czas wykonania: {end_time - start_time:.4f} s")

if __name__ == "__main__":
    main()