class Family(object):
    def __init__(self, world, **kwargs):
        self.world  = world
        self.size   = kwargs['size']
        self.id     = kwargs['id']
        self.x      = kwargs['x']
        self.y      = kwargs['y']
        self.buildingId = 0
        self.occupants = []
    
    def setOccupants(self, listOfOccpants):
        self.occupants = listOfOccpants

    def addOccupants(self, id):
        self.occupants.append(id)

    def changeLocation(self, newX, newY):
        self.x = newX
        self.y = newY
        for occupantId in self.occupants:
            self.world.population[occupantId - 1].familyX = newX
            self.world.population[occupantId - 1].familyY = newY