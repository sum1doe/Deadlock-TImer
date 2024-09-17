try:
    cfg = open("config.txt", "r").read().split("\n")
    
except FileNotFoundError:
    print("Creating cfg file")
    cfg = open("config.txt", "w+")
    config_string = "[Keys]\ntimer_reset:96\ntimer_pause:97\noverlay_hide:99\nscroll_activation:46\n"
    config_string += "[Positions]\nscreen_size_x:1600\nscreen_size_y:900\ntimer_x:935\ntimer_y:20\nmessage_x:800\nmessage_y:300\n"
    cfg.write(config_string)
    cfg.close()
    cfg = config_string
    
finally:
    dict_sub_string = ""
    config = {}
    for i in cfg:
        i = i.strip()
        if len(i) == 0:
            continue
        if i[0] == "[" and i[-1] == "]":
            dict_sub_string = i[1:-1]
            config[dict_sub_string] = {}
        else:
            a,b = i.split(":")
            config[dict_sub_string][a] = int(b)  