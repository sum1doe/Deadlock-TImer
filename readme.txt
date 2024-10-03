Requirements:
 - Windows 10 (11 should work, but no guarantees)
 - Python 3.10+ (Coded and tested with Python 3.12.5. Python has a website, you know how to look for the downloads tab.)
 - The following python modules installed. (Once you've installed python, run "pip install [module]" to install these)
   - pygame
   - pywin32
   - pynput
   - ctypes

How to use:
 - Assuming you've just installed python for the first time ever, open the "Deadlock Overlay.py" file with "IDLE (Python 3.x.x)".
 - At the top, there is a Run tab (next to File, 4th option over). Click that, and then "Run Module". Alternatively just hit f5 while in the window.
 - Currently, the program should just run, assuming you meet all the requirements.
 - To close, you'll need to stop running the code, by closing the shell window. Ctrl + C in the shell works too, but is may be unstable.
 - Optionally, edit the config.txt file and restart the code.

Default Keybindings:
 - Numpad 0 resets the timer.
 - Numpad 1 pauses it.
 - Numpad 3 hides/shows the overlay, and reloads settings from the config on press.
 - Hold delete and scroll (yes, turn the wheel on your mouse, or if you're on a touchpad, use the 2 finger trick) to adjust the timer by the second.