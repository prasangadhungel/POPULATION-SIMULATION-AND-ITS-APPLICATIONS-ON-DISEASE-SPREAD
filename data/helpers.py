import random 

def flip(x):
    num = random.random()
    if num > x :
        return True
    return False

def distance(item1, item2):
    return ((item1['x'] - item2['x'])**2 + (item1['y'] - item2['y']) ** 2) ** 0.5

