import subprocess

command = "uvicorn app.main:app --port=8000"
subprocess.run(command, shell=True)

