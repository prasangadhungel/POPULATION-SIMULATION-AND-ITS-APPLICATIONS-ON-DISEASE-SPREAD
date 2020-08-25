from bt import *
import json
import pickle
from data.population import generatePopulation, generatePopulationfromFile
from data.places import generateBuildingsfromFile
from data.configuration import INFECTION_PERIOD
import pandas as pd
import os
import errno

outputs = []
infection_counts = []

simulationiteration = 0
numberOfIteration   = 5
numberOfTimeSteps   = 160
visitedQueue = []
SIMULATION_TIME_STEP = 1
config_dictionary = {"map_image": "koniyosomMap.png", "iteration_count": numberOfIteration, "time_steps":numberOfTimeSteps}
with open("config.json", 'w') as fp:
    json.dump(config_dictionary, fp)

class World(object):
    population = []
    vehicles   = []
    markets    = []
    visitables = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Start world parameters.
        # Read from a configuration file to start world parameters.
        # Read population data.
        # Read Map, Road and Buildings data.
        # Generate appropriate IDs and stuff for buildings, people and assign them with attributes
        # according to the configuration file. Then continue to the simulation model.

        # Start with necessary parameters for the world
        self.time = 0
        # simulationParams= open("simulationparams.txt", 'r')       
        # self.maleInteraction = 0
        # self.FemaleInteraction = 0
        # self.educationInteraction = [0]*21
        # for i in range(9):
        #     self.educationInteraction[i] -= random.randint(200,500) 
        # for i in range(11, 21):
        #     self.educationInteraction[i] += i *random.randint(1,2) 

        # self.ageInteraction =[0]*90
        # for i in range(4):
        #     self.ageInteraction[i] = 1000 + random.randint(1000,2000)
        # self.ageInteraction[20] = 4000
        # for i in range(52,90):
        #     self.ageInteraction[i] = 1500 - 5 * i - random.randint(0,300)
        self.buildings  = generateBuildingsfromFile(self, 'real_input/Buildings.csv')
        self.visitables = [self.buildings[item].id for item in self.buildings if self.buildings[item].special]

        self.population= generatePopulationfromFile(self, 'real_input/PopulationKoniyosom.csv')
        infectedcount = 0
        for item in self.population:
            if item.infected == True:   
                infectedcount += 1

        print("Total Population:", len(self.population))
        print("Infected Count At beginning: ", infectedcount)


        # assignBuildings(self)
        # Completed processing buildings
        # Group people according to age into different age groups and assign them their own special buildings.
       
        self.schools = [self.buildings[item] for item in self.buildings if  self.buildings[item].type == 'school']
        self.workplaces = [self.buildings[item] for item in self.buildings if  self.buildings[item].type == 'market']

        self.roads = generateRoads_and_RoadNodesFromFile(self, 'real_input/RoadNodes.csv', 'real_input/Roads.csv')       
        self.vehicles = generateVehicles(self)
       

        
    def simulate(self):
        if (self.time - 25) % (7 * 24)  == 0:
            print("Not saturday, workday starts")
            for items in self.population:
                items.checked = False

        self.time += SIMULATION_TIME_STEP
        updateAllVehicles(self)            
        buildingInteraction(self)

        for entity in self.population:
            BT = behaviorTree[entity.type]
            # Change the state of entity and update as the output of BT processing.
            BT(self, entity)

        print("Time End:", self.time)
        infectedcount = 0
        Humansl = [{'infected': bool(item.infected), 'x': item.x, 'y': item.y} for item in self.population]        
        Vehiclel = [{'x': item.x, 'y': item.y} for item in self.vehicles]
        outdict = {'Human': Humansl, 'Vehicle':Vehiclel}
        for item in self.population:            
            if item.infected == True:
                item.infectionTime += 1
                if item.infectionTime > INFECTION_PERIOD:
                    item.infected = False
                    item.infectionTime = 0
                    item.hasBeenInfected = True
                    item.susceptibility /= 200   
                infectedcount += 1
        infection_counts.append(infectedcount)
        print("Infected Count: ", infectedcount)
        
        # time.sleep(0.2)


        if self.time > numberOfTimeSteps:
            pass

        else:
            filename = "logs/iteration_count"+str(simulationiteration+1)+"/time_steps"+str(self.time)+".json"
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            
            with open(filename, 'w') as fp:
                json.dump(outdict, fp)
            time.sleep(0.5)
            self.simulate()

    def analyse(self):
        pass
        # print(self.maleInteraction, self.FemaleInteraction,self.educationInteraction,self.ageInteraction)
        # numedu = [0]*21
        # for item in self.population:
        #     numedu[item.education] += 1

        # numage = [1]*90
        # for item in self.population:
        #     numage[item.age] += 1



if __name__ == "__main__":
    for simulationiteration in range(numberOfIteration):
        w = World()
        w.simulate()
        outputs.append({"runLabel": str(simulationiteration), "data":infection_counts})
        infection_counts = []
        with open("multirun.js", 'w') as fp:
            fp.write("var outputs = "+ str(outputs))
        # w.analyse()

