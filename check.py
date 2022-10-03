import json
import socket
from concurrent.futures import ThreadPoolExecutor, wait


servers = json.loads(open("servers.json", "r").read())

assert isinstance(servers, dict)


def run_test(host, config):
    print('Running test for', host)
    for p in ("t"):
        if port := config.get(p):
            sock = socket.socket()
            print("Attempting to connect to:", host, port, p)
            try:
                sock.connect((host, int(port)))
                print("Connection OK to", host, port)
                sock.settimeout(3)
                sock.send(b'{"jsonrpc":"2.0","method":"server.version","id":0,"params":{"client_name": "pybitcointools", "protocol_version": "1.4"}}')
                print('Message sent to', host, port)
                try:
                    received = sock.recv(1024)
                    print("Received from", host, port, ": ", received.decode())
                except TimeoutError:
                    print("No Message received from", host, port)
                sock.close()
            except ConnectionRefusedError:
                print('Could not connect to', host, port)


for host, config in servers.items():
    fs = []
    with ThreadPoolExecutor() as executor:
        f = executor.submit(run_test, host, config)
        fs.append(f)
    wait(fs)
