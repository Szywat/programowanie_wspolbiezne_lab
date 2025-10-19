import os
import time

bd = "bufor.txt"
ld = "lockfile"
end = ";"

print("Server is running...")

while True:
    if os.path.exists(ld) and os.path.exists(bd) and os.path.getsize(bd) > 0:
        try:
            with open(bd, "r") as bufor:
                lines = bufor.readlines()

            # pierwsza linia to nazwa pliku klienta
            cf = lines[0].strip()
            # pozostałe linie to wiadomość (bez znacznika końca)
            message_lines = [line.strip() for line in lines]
            message = "\n".join(message_lines)

            print("Received message:\n")
            print(f"{message}\n")

            print("Message to client (end with new line): ")
            response_lines = []
            while True:
                line = input()
                if line == "":
                    break
                response_lines.append(line)
            response = "\n".join(response_lines)

            with open(cf, "w") as f:
                f.write(response + "\n")
                f.write(end + "\n")

            print(f"Response sent.")

            os.remove(ld)
            with open(bd, "w") as bufor:
                bufor.write("")

        except Exception as e:
            print(f"Error: {e}")

    time.sleep(1)