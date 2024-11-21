import pygame
from os import environ

import win32api
import win32con
import win32gui

import ctypes

from message_gen import relevant_message
from config_parser import config as user_config

awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
print(awareness.value)

# Set DPI Awareness  (Windows 10 and 8)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
print(errorCode)


environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)

pygame.init()
wx, wy = user_config["Positions"]["screen_size_x"], user_config["Positions"]["screen_size_y"]

screen = pygame.display.set_mode((wx,wy), pygame.NOFRAME) # For borderless, use pygame.NOFRAME

done = False
fuchsia = (255, 0, 128)  # Transparency color
dark_red = (139, 0, 0)
blue = (0, 0, 255)
white = (255,255,255)
black = (0,0,0)


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)



# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(hwnd, -1, 0,0,wx,wy, 2|1)

clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(fuchsia)  # Transparent background
    
    pygame.draw.rect(screen, white, pygame.Rect(wx//2, wy//2, 2, 2))
    pygame.draw.rect(screen, black, pygame.Rect(wx//2, wy//2+1, 1, 1))
    pygame.draw.rect(screen, black, pygame.Rect(wx//2+1, wy//2, 1, 1))
    
    pygame.display.update()
    clock.tick(1)
