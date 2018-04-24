import cassiopeia as cass
ONLINE = True

def get_summoner(region, name):
    print(region)
    print(name)
    print(ONLINE)
    print("test")
    return cass.Summoner(region=region, name=name)
