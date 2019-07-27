import random 

def flip(x):
    num = random.random()
    if num < x :
        return True
    return False

def distance(item1, item2):
    return ((item1.x - item2.x)**2 + (item1.y - item2.y) ** 2) ** 0.5

def findClosest(entity, listToSearch):
    minDistance = 1000000000
    minId       = 0
    for item in listToSearch:
        if distance(item, entity) < minDistance:
            minId = item.id
            minDistance = distance(item, entity)
        
    return minId

def updateAllVehicles(world):
    for vehicle in world.vehicles:
        vehicle.update(world)

def buildingInteraction(world):
    for building in world.buildings:
        building.interact()