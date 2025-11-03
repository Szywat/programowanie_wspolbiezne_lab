
import os
import sys
import re
import time

def count_words_in_file(filename, word):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read() # read the file

        words = re.findall(r'\b\w+\b', content.lower()) # finds all words matching the regex
        count = words.count(word.lower()) # counts how many times the word appeared

        input_pattern = r'\\input\{([^}]+)\}' # creates the \input pattern
        input_files = re.findall(input_pattern, content) # creates a list of filenames

        # Store all child processes info to wait for them later
        children = []

        # Create all child processes first (they run in parallel)
        for input_file in input_files:
            read_fd, write_fd = os.pipe() # creates a pipe with two channels - read, write

            pid = os.fork() # forks the process into main process and child process

            if pid == 0:  # Child process
                time.sleep(1)
                print(f"Child process PID: {os.getpid()} processing file: {input_file}")
                os.close(read_fd) # closes the read channel as it's not needed

                child_count = count_words_in_file(input_file, word) # repeat the process as there are more files to read

                os.write(write_fd, str(child_count).encode()) # writes the output of the file to the write channel
                os.close(write_fd) # closes the write channel

                exit_status = min(child_count, 255) # exits
                sys.exit(exit_status) # exits with appropriate status
            else: # Parent process
                print(f"Parent process PID: {os.getpid()} created child PID: {pid} for {input_file}")
                os.close(write_fd) # close write end in parent
                # Store child info (pid and read file descriptor)
                children.append((pid, read_fd))

        # Now wait for ALL children to finish
        for pid, read_fd in children:
            # time.sleep(1)
            print(f"Parent process PID: {os.getpid()} waiting for child PID: {pid}")

            child_pid, status = os.wait()

            if os.WIFEXITED(status):
                exit_status = os.WEXITSTATUS(status)
                # time.sleep(1)
                print(f"Child process {child_pid} exited normally with status: {exit_status}")

                child_count_bytes = os.read(read_fd, 1024)
                os.close(read_fd)

                if child_count_bytes:
                    child_count = int(child_count_bytes.decode())
                    count += child_count
                    # time.sleep(1)
                    print(f"Child process {child_pid} contributed count: {child_count}")

            elif os.WIFSIGNALED(status):
                # time.sleep(1)
                print(f"Child process {child_pid} was terminated by signal")
                os.close(read_fd)
            else:
                # time.sleep(1)
                print(f"Child process {child_pid} terminated abnormally")
                os.close(read_fd)

        return count

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found", file=sys.stderr)
        return 0
    except Exception as e:
        print(f"Error processing file '{filename}': {e}", file=sys.stderr)
        return 0


def main(p, s):
    print(f"Main process PID: {os.getpid()} starting to process file: {p}")
    time.sleep(3)
    count = count_words_in_file(p, s)
    result = f"word: {s}, count: {count}"
    return result


if __name__ == "__main__":
    result = main('plikA.txt', 'i')
    print(result)