#!/usr/bin/python
import os
import sys
if os.name == 'nt':
    import msvcrt
    from msvcrt import getch as _win_getch
else:
    import tty
    import termios

class GetPass:

    def _unix_getch(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def getpass(self, prompt='Password : ', stream=None):
        """Prompt for password with echo off, using Unix getch()."""
        password = ""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while 1:
            c = _win_getch() if os.name == 'nt' else self._unix_getch()
            if c == b"\r" or c == b"\n":
                break
            if c == "\003":
                raise KeyboardInterrupt
            if c == b"\b":
                c = ""
            password += c.decode('utf-8')
            sys.stdout.write("*")
            sys.stdout.flush()    
        return password
