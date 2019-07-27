import random
from data.configuration import INFECTION_SPREAD
import time

class Vehicle(object):
    """
    Vehicle in simulation kwargs: id, (bool), x, y
    """
    def __init__(self, world,  **kwargs):
        """
        Parameters:
        """
        self.id             = kwargs["id"]            
        self.roadId         = kwargs['roadId']
        curNode             = world.roads[self.roadId - 1].currentNode
        self.x              = curNode.data.x
        self.y              = curNode.data.y
        self.world          = world
        self.currentNode    = curNode
        self.prevNode       = curNode.prev
        self.nextNode       = curNode.next
        self.direction      = random.randint(0,1)
        if self.direction == 0:
            if self.nextNode != None:
                self.destNode = self.nextNode
            else:
                self.destNode  = self.prevNode
                self.direction = 1 - self.direction
        
        else:
            if self.prevNode != None:
                self.destNode = self.prevNode
            else:
                self.destNode  = self.nextNode
                self.direction = 1 - self.direction 

        self.moving         = True
        self.stoppedsince   = 0
        self.speed          = random.randint(5, 10)
        self.passengers     = []


    def addPassenger(self, entity):
        self.passengers.append(entity)
    
    def dropPassenger(self, entity):
        for i in range(len(self.passengers)):
            if self.passengers[i].id == entity.id:
                self.passengers.pop(i)
                break

    def move(self, world):
        delx  = self.destNode.data.x - self.x
        dely  = self.destNode.data.y - self.y
        steps = int(max(abs(delx), abs(dely))) // self.speed
        if steps > 0:
            self.x += delx/steps
            self.y += dely/steps
            # print("Vehicle", self.id," is at location: ", self.x, self.y)
            # time.sleep(0.05)
            for items in self.passengers:
                items.x = self.x
                items.y = self.y
                # print("Human", items.id, " is at: ", self.x, self.y)

        else:
            self.x = self.destNode.data.x
            self.y = self.destNode.data.y
            for items in self.passengers:
                items.x = self.x
                items.y = self.y
                # print("Human", items.id, " is at: ", self.x, self.y)

            # print("Vehicle", self.id, "Stopped at: ", self.x, self.y)
            # time.sleep(1)
            self.moving = False
            for item in self.passengers:
                if ((item.destination.x - self.x)**2 + (item.destination.y - self.y) ** 2) ** 0.5 < 50:
                    print("Human", item.id, "has reached destination")
                    # time.sleep(1)
                    item.isDelegated = False
                    item.delegator = None
                    self.dropPassenger(item)
                    item.x = item.destination.x
                    item.y = item.destination.y
                    item.reachedDestination = True
                    if item.destination.id == item.homeId:
                        # print("Reached Home: ", item.id)
                        pass
                    item.destination.occupants.append(item)

            self.currentNode = self.destNode
            if self.direction == 0:
                if self.nextNode != None:
                    self.destNode = self.nextNode
                else:
                    self.destNode  = self.prevNode
                    self.direction = 1 - self.direction
            
            else:
                if self.prevNode != None:
                    self.destNode = self.prevNode
                else:
                    self.destNode  = self.nextNode
                    self.direction = 1 - self.direction 

            self.nextNode = self.currentNode.next
            self.prevNode = self.currentNode.prev
            if world.time < 14 or len(self.passengers) > 0:
                self.moving = True

    def interact(self):
        # print(len(self.passengers), "interacting in vehicle: ", self.id)        
        for item1 in self.passengers:
            if item1.infected == True:
                for item2 in self.passengers:
                    if item2.infected == False:
                        item2.infected = random.random() < INFECTION_SPREAD

    def update(self, world):
        self.interact()
        if self.moving:
            self.move(world)
        else:
            if world.time < 14 or len(self.passengers) > 0:
                self.moving = True


    def setPassengers(self, listOfPassengers):
        self.passengers = listOfPassengers

    