from bt import *
import json
import pickle
from matplotlib import pyplot as plt
from data.population import generatePopulation, generatePopulationfromFile
from data.places import generateBuildings, generateBuildingsfromFile
from data.configuration import INFECTION_PERIOD
import pandas as pd
import numpy as np
import os
import errno



simulationiteration = 0
numberOfIteration   = 3
numberOfTimeSteps   = 100
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
       
        # DictionaryList  = []
        # Index = []
        # for item in self.population:
        #     dict = {'familyId': item.familyId, 'homeId': item.homeId, 'schoolId': item.schoolId, 'workplaceId': item.workplaceId,  
        #             'age':item.age, 'sex': item.sex, 'infected':item.infected, 'infectionTime': item.infectionTime,
        #             'type': item.type, 'education': item.education, 'homeX': item.homeX, 'homeY':item.homeY, 'susceptibility': item.susceptibility}
        #     Index.append(item.id)
        #     DictionaryList.append(dict)
        # df = pd.DataFrame(DictionaryList, index = Index)
        # df.to_csv('inputs/Population.csv')

        # DictionaryList = []
        # Index = []
        # for item in self.roads:
        #     nodelis = [ids.id for ids in item.nodes]
        #     dict = {'nodes': str(nodelis)}
        #     DictionaryList.append(dict)
        #     Index.append(item.id)

        # df = pd.DataFrame(DictionaryList, index = Index)
        # df.to_csv('Roads.csv')
        # DictionaryList = []
        # Index = []
        # for item in self.roadNodes:
        #     dict = {'x': item.x, 'y':item.y}
        #     DictionaryList.append(dict)
        #     Index.append(item.id)

        # df = pd.DataFrame(DictionaryList, index = Index)
        # df.to_csv('RoadNodes.csv')
        
        # DictionaryList = []
        # Index = []
        # for item in self.buildings:
        #     occupantsids = [ids.id for ids in item.occupants]
        #     dict = {'special': item.special, 'type':item.type, 'interaction_time':item.interaction_time, 'x':item.x, 'y':item.y,
        #             'occupants': str(occupantsids)}
        #     DictionaryList.append(dict)
        #     Index.append(item.id)

        # df = pd.DataFrame(DictionaryList, index = Index)
        # df.to_csv('Buildings.csv')
        # exit(0)
        # Feature assignment has already been done. We just need to start the simulation.
        # plt.figure(figsize=(50, 50))      
        # for item in self.roadNodes:
        #     plt.scatter(item.x, item.y, s = 100, c = (0,1,0), alpha = 0.5)   

        # for road in self.roads:
        #     for i in range(len(road.nodes) - 1):
        #         plt.plot((road.nodes[i].x, road.nodes[i + 1].x), (road.nodes[i].y, road.nodes[i + 1].y), c = (0,0,1), alpha = 0.5)

        # for vehicl in self.vehicles:
        #     plt.scatter(vehicl.x, vehicl.y, marker='^',s = 75,  c = (0,1,1), alpha=0.5)

        # for vehicl in self.population:
        #     if vehicl.infected == True:
        #         plt.scatter(vehicl.x, vehicl.y, s = 1,  c = (1,0,0), alpha=1)
        #     else:
        #         plt.scatter(vehicl.x, vehicl.y, s = 1,  c = (1,1,0), alpha=1)

        # plt.title('Roads = Line , RodeNodes = Circle, Vehicles= Red Triangle')    
        # plt.show()

        
    def simulate(self):
        # plt.figure(figsize=(1000, 1000))      

        # for road in self.roads:
        #     for i in range(len(self.roads[road].nodes) - 1):
        #         plt.plot((self.roads[road].nodes[i].x, self.roads[road].nodes[i + 1].x), (self.roads[road].nodes[i].y, self.roads[road].nodes[i + 1].y), c = 'blue', alpha = 0.5)

        # for vehicl in self.vehicles:
        #     plt.scatter(vehicl.x, vehicl.y, marker='^',s = 50,  c = 'green')

        # for vehicl in self.population:
        #     if vehicl.infected == True:
        #         plt.scatter(vehicl.x, vehicl.y, s = 1,  c = 'red', alpha=1)

        # plt.show()

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
        Vehiclel = [{'x': item.x, 'y': item.y, 'passengers': [ids.id for ids in item.passengers]} for item in self.vehicles]
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
        # print(self.maleInteraction, self.FemaleInteraction,self.educationInteraction,self.ageInteraction)
        # numedu = [0]*21
        # for item in self.population:
        #     numedu[item.education] += 1

        # numage = [1]*90
        # for item in self.population:
        #     numage[item.age] += 1

        plt.bar(np.arange(len(numage)), [x/y for x, y in zip(self.ageInteraction, numage)],width=0.4, color = 'b',align='center')
        plt.show()

if __name__ == "__main__":
    for simulationiteration in range(numberOfIteration):
        w = World()
        w.simulate()
        # w.analyse()

