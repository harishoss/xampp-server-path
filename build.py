import subprocess

SUBPROCESS_CALLS = [
    "sudo rm /usr/local/bin/xampp-root",
    "chmod -x xampp-root.py",
    "sudo cp xampp-root.py /usr/local/bin/xampp-root",
    "sudo chmod a+x /usr/local/bin/xampp-root"
]

for command in SUBPROCESS_CALLS:
    commandParts = command.split(' ')
    subprocess.call(commandParts)
