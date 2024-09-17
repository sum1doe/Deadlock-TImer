import pygame
from os import environ

import win32api
import win32con
import win32gui

from pynput import mouse

import ctypes

awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
print(awareness.value)

# Set DPI Awareness  (Windows 10 and 8)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(2)
print(errorCode)


environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)

pygame.init()
wx, wy = 1600,900

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

def relevant_message(ms):
    match(ms):
        case ms if ms < 0:
            return "How did you get here?"
        case ms if ms <= 15000:
            return "Game Start"
        case ms if ms >= 2*60000 and ms <= 2.25*60000:
            return "Small Camp (45 souls/4 mins) has spawned"
        case ms if ms >= 3*60000 and ms <= 3.25*60000:
            return "Boxes and Statues have spawned"
        case ms if ms >= 6*60000 and ms <= 6.25*60000:
            return "Small Camp *should* have respawned. If you remembered to take it."
        case ms if ms >= 7*60000 and ms <= 7.25*60000:
            return "Medium (95 souls/6 mins) and Hard Camps (250 souls/8 mins) have spawned."
        case ms if ms >= 10*60000 and ms <= 10.25*60000:
            return "10 Minutes. Soul change, Midboss, Urn in 30s"
        case ms if ms >= 10.5*60000 and ms <= 10.75*60000:
            return "Soul urn has touched grass"
    pass


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

prev_lst = [False for i in range(1024)]

mouse_listener = mouse.Listener(on_scroll = on_mouse_scroll)
mouse_listener.start()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
    #Num0 96 for reset
    if isKeyPressed(96):
        start = pygame.time.get_ticks()
        
    #Num1 97 for pause/play
    if not isKeyPressed(97):
        Num1Pressed = False
    
    # Check that key has been unpressed, and state is currently unpaused
    if not Num1Pressed and unpaused and isKeyPressed(97):
        offset = current_time
        unpaused = False
        Num1Pressed = True
        
    if not Num1Pressed and not unpaused and isKeyPressed(97):
        start = pygame.time.get_ticks()-offset
        unpaused = True
        Num1Pressed = True
        
    #Num3 99 for toggle overlay
    if not isKeyPressed(99):
        Num3Pressed = False
        
    if not Num3Pressed and isKeyPressed(99):
        showhud = not showhud
        Num3Pressed = True
        
    
    #Delete 46 for chording with scroll
    modPressed = isKeyPressed(46)
    
    #MMB 4 for something happened.
    

    screen.fill(fuchsia)  # Transparent background
    
    
    current_time = pygame.time.get_ticks()-start
    
    
    number_image = number_font.render(formatms((offset, current_time)[unpaused]), False, (255,255,255))
    notif = number_font.render(relevant_message((offset, current_time)[unpaused]), False, (255,255,255))
    if showhud:
        #pygame.draw.rect(screen, (dark_red, blue)[isKeyPressed(65)], pygame.Rect(0, 0, 60, 60))
        screen.blit(notif, (800,300))
        screen.blit(number_image, (935, 20))
    
    pygame.display.update()
    
    clock.tick(15)
