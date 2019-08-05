import random
# from data.configuration import INFECTED_AT_START, INFECTION_PERIOD, INFECTION_SPREAD
# import pandas as pd
# import numpy as np 

class Human(object):
    age = 0
    def __init__(self, world, **kwargs):
        '''
            Humans are super class for all the interacting entities in the population simulation.
            They can be of the following types:
            1. Student
            2. Working
            3. Toddler
            4. Elderly
            5. Housewife
        '''
        try:
            self.type           = kwargs['type']
        except:
            self.type           = ""

        self.world              = world
        self.id                 = kwargs['id']
        self.familyId           = kwargs['familyId']
        try:
            self.x                  = kwargs['homeX']
            self.y                  = kwargs['homeY']
            self.homeX              = kwargs['homeX']
            self.homeY              = kwargs['homeY']

        except:
            self.x                  = 0
            self.y                  = 0
            self.homeX              = 0
            self.homeY              = 0


        try:
            self.education          = kwargs['education']
        except:
            self.education          = 0

        try:
            self.age            = kwargs['age']
        except:
            self.age            = 0
    
        self.simulated          = False
        try:
            self.sex            = kwargs['sex']
        except:
            self.sex            = 'Male' if random.randint(0,1) == 0 else 'Female'

        self.isDelegated        = False
        self.delegating         = False
        self.delegator          = None
        self.checked            = False
        self.readyToTravel      = False
        self.reachedDestination = False
        self.destination        = None
        self.destinationTime    = 0
        self.destinationX       = None  # Set a building type as destination.    
        self.destinationy       = None
        self.vehicleId          = 0
        try:
            self.homeId         = kwargs['homeId']
        except:
            self.homeId         = 0
        
        try:
            self.schoolId         = kwargs['schoolId']
        except:
            self.schoolId         = 0

        try:
            self.workplaceId      = kwargs['workplaceId']
        except:
            self.workplaceId      = 0

        self.ownsVehicle        = False
        
        try:
            self.infected       = kwargs['infected'] 
        except:
            self.infected           = random.random() < INFECTED_AT_START
        
        try:
            self.susceptibility = kwargs['susceptibility'] / 5
        except:
            try:
                xx = [self.age, int(self.sex == 'Male'), self.education]
                xx = np.array([xx])
                self.susceptibility = netModel.predict(xx)[0][0]/1000000
                #1000000
            except:
                self.susceptibility = random.random() < INFECTION_SPREAD

        try:
            self.infectionTime      = kwargs['infectionTime']

        except:
            if self.infected:
                self.infectionTime  = random.randint(1, INFECTION_PERIOD)
            else:
                self.infectionTime      = 0

    def atHome(self):
        return ( abs(self.homeX - self.x) <= 0.0001 and abs(self.homeY - self.y) <= 0.0001)

    def __str__(self):
        return self.id

    def getType(self):
        return self.type

    def setType(self, type):
        self.type = type
