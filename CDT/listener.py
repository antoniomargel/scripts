#!/usr/bin/env python3
"""
listener.py
Author: amm2825
Description: Basic listener for remote shell
"""

import socket

def main():
    host = "0.0.0.0"
    port = 8443  # or any open port you choose
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"[+] Listening on {host}:{port}")
    client_socket, addr = server_socket.accept()
    print(f"[+] Connection from {addr}")

    while True:
        command = input("Shell> ")
        if command.strip() == "":
            continue
        client_socket.sendall(command.encode())
        if command.lower() == "exit":
            break
        data = client_socket.recv(4096)
        print(data.decode(), end="")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
