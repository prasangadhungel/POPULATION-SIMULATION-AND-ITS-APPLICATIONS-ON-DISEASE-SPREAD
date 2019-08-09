import random
import math
from data.configuration import INFECTION_PERIOD

class Building(object):
    """
    Building in simulation kwargs: id, special (bool), x, y
    """
    def __init__(self, world,  **kwargs):
        """
        Parameters:
        """
        try:
            self.type = kwargs['type']
        except:
            self.type = 'normal'

        self.id = kwargs["id"]

        try:
            self.special = kwargs['special']
        except: 
            self.special = False

        try:            
            self.x  = kwargs['x']
            self.y  = kwargs['y']
        except:
            self.x  = 0
            self.y  = 0

        self.occupants = []
        self.world = world
        if self.special:
            try:
                self.interaction_time = kwargs["interaction_time"]
            except:
                self.interaction_time = random.randint(3,6)
        
        else:
            try:
                self.interaction_time = kwargs['interaction_time']
            except:
                self.interaction_time = 30000000
    def addOccupant(self, entity):
        self.occupants.append(entity)
    
    def dropOccupant(self, entity):
        for i in range(len(self.occupants)):
            if self.occupants[i].id == entity.id:
                self.occupants.pop(i)
                break

    def interact(self):
        # print(len(self.occupants), "interacting in building: ", self.id)
        for item1 in self.occupants:
            if item1.infected == True:
                for item2 in self.occupants:
                    if item2.infected == False:                
                        item2.infected = (random.random() < item2.susceptibility / (1 + 10 * self.world.time  / ( 1 + math.exp(random.randint(40,50) - self.world.time)))) 
                        if item2.infected:
                            item2.infectionTime = random.randint(0, INFECTION_PERIOD/2)


    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type
        
    def setOccupants(self, listOfOccupants):
        self.occupants = listOfOccupants