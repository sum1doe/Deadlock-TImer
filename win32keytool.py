import win32api

#Ctrl + C to exit.

def isKeyPressed(key):
    #"if the high-order bit is 1, the key is down; otherwise, it is up."
    
    return (win32api.GetAsyncKeyState(key) & (1 << 15)) != 0

prev_lst = [False for i in range(1024)]

while True:
    lst = [isKeyPressed(i) for i in range(1024)]
    for i in range(1024):
        if prev_lst[i] != lst[i]:
            print(i, chr(i))
    prev_lst = lst