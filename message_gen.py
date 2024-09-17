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