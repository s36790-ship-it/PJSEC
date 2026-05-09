## To setup project

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## To start server

```bash
cd server
flask --app main run
```

## To start agent (with python)

```bash
cd agent
python agent.py
```

## To build agent with pyinstaller

```bash
cd agent
python -m pyinstaller agent.py -w -F
```
Builds agent.exe that runs in background (on Windows, pyinstaller creates exectuable based on system its running on)
