import threading
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=False)
    process.wait()
    print(f"Command '{' '.join(command)}' completed with return code {process.returncode}")

if __name__ == "__main__":
    commands_with_args = [
        ["python", "2_dewarp.py", "0"],
        ["python", "2_dewarp.py", "1"],
        ["python", "2_dewarp.py", "2"],
        ["python", "2_dewarp.py", "3"],
        ["python", "2_dewarp.py", "4"],
        ["python", "2_dewarp.py", "5"],
    ]

    threads = []
    for command in commands_with_args:
        thread = threading.Thread(target=run_command, args=(command,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    print("All commands have been executed.")
