import pygame
from os import environ

import win32api
import win32con
import win32gui

from pynput import mouse

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
wx, wy = user_config["Positions"]["screen_size_x"],user_config["Positions"]["screen_size_y"]

screen = pygame.display.set_mode((wx,wy), pygame.NOFRAME) # For borderless, use pygame.NOFRAME

done = False
fuchsia = (255, 0, 128)  # Transparency color
dark_red = (139, 0, 0)
blue = (0, 0, 255)


# Create layered window
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)



# Set window transparency color
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
win32gui.SetWindowPos(hwnd, -1, 0,0,wx,wy, 2|1)

# Function Box
def isKeyPressed(key):
    #"if the high-order bit is 1, the key is down; otherwise, it is up."
    
    return (win32api.GetAsyncKeyState(key) & (1 << 15)) != 0

def on_mouse_scroll(mouse_position_x, mouse_position_y, scroll_x_change, scroll_y_change):
    global start, offset, modPressed
    start += scroll_y_change*-1000*modPressed
    offset += scroll_y_change*-1000*modPressed
    
def formatms(ms):
    s = ms//1000
    if ms >= 0:
        m = s//60
        s = s=s%60
        return f"{m:>4}:{s:>3}"
    return f"{s:>8}"

# Timer things
clock = pygame.time.Clock()
number_font = pygame.font.Font(None, 24)
start = pygame.time.get_ticks()

offset = 0
unpaused = True
Num1Pressed = False
Num3Pressed = False

showhud = True
active = False

mouse_listener = mouse.Listener(on_scroll = on_mouse_scroll)
mouse_listener.start()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #Num0 96 for reset
    if isKeyPressed(user_config["Keys"]["timer_reset"]):
        start = pygame.time.get_ticks()
        
    #Num1 97 for pause/play
    if not isKeyPressed(user_config["Keys"]["timer_pause"]):
        Num1Pressed = False
    
    # Check that key has been unpressed, and state is currently unpaused
    if not Num1Pressed and unpaused and isKeyPressed(user_config["Keys"]["timer_pause"]):
        offset = current_time
        unpaused = False
        Num1Pressed = True
        
    if not Num1Pressed and not unpaused and isKeyPressed(user_config["Keys"]["timer_pause"]):
        start = pygame.time.get_ticks()-offset
        unpaused = True
        Num1Pressed = True
        
    #Num3 99 for toggle overlay
    if not isKeyPressed(user_config["Keys"]["overlay_hide"]):
        Num3Pressed = False
        
    if not Num3Pressed and isKeyPressed(user_config["Keys"]["overlay_hide"]):
        showhud = not showhud
        Num3Pressed = True
        
    
    #Delete 46 for chording with scroll
    modPressed = isKeyPressed(user_config["Keys"]["scroll_activation"])
    
    #MMB 4 for something happened.
    

    screen.fill(fuchsia)  # Transparent background
    
    
    current_time = pygame.time.get_ticks()-start
    
    
    timer_obj = number_font.render(formatms((offset, current_time)[unpaused]), False, (255,255,255))
    message_obj = number_font.render(relevant_message((offset, current_time)[unpaused]), False, (255,255,255))
    if showhud:
        #pygame.draw.rect(screen, (dark_red, blue)[isKeyPressed(65)], pygame.Rect(0, 0, 60, 60))
        screen.blit(timer_obj, (user_config["Positions"]["timer_x"], user_config["Positions"]["timer_y"]))
        screen.blit(message_obj, (user_config["Positions"]["message_x"], user_config["Positions"]["message_y"]))
    
    pygame.display.update()
    
    clock.tick(15)
