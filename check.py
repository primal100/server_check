import json
import socket


servers = json.loads(open("servers.json", "r").read())

assert isinstance(servers, dict)

for host, config in servers.items():
    sock = socket.socket()
    for p in ("t", "s"):
        if port := config.get(p):
            print("Attempting to connect to:", host, port, p)
            sock.connect((host, int(port)))
            print("Connection OK")
