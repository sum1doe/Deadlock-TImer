def get_soul_value(time):
    """Returns a dict of soul values for the given parameter time.
    time is in ms"""
    
    base_dict = {
        "trooper":75,
        "guardian":275,
        "walker":750,
        "shrine":500,
        "patron":500,
        "small_creep":44,
        "medium_creep":88,
        "large_creep":220,
        "sinners_sacrifice":330,
        "crate":36,
        "soul_urn":2500,
        "hero":225
    }
    
    growth_dict = {
        "trooper":1.1,
        "guardian":0,
        "walker":0,
        "shrine":0,
        "patron":0,
        "small_creep":0.528,
        "medium_creep":1.06,
        "large_creep":2.64,
        "sinners_sacrifice":3.96,
        "crate":3,
        "soul_urn":100,
        "hero":26
    }
    
    return {i:round(base_dict[i]+growth_dict[i]*time/1000, 0) for i in base_dict.keys()}
    
print(get_soul_value(60000)["trooper"])