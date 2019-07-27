from bt import *
import json
import pickle
from matplotlib import pyplot as plt
from data.population import generatePopulation, generatePopulationfromFile
from data.places import generateBuildings, generateBuildingsfromFile
from data.configuration import INFECTION_PERIOD
import pandas as pd

visitedQueue = []
SIMULATION_TIME_STEP = 1
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
        self.population, self.families = generatePopulationfromFile(self, 'Population.csv')
       
        infectedcount = 0
        for item in self.population:
            if item.infected == True:   
                infectedcount += 1

        print("Total Population:", len(self.population))
        print("Infected Count At beginning: ", infectedcount)
       
        self.buildings  = generateBuildingsfromFile(self, 'Buildings.csv')
        self.visitables = [item.id for item in self.buildings if item.special]
       
        assignBuildings(self)
        # Completed processing buildings
        # Group people according to age into different age groups and assign them their own special buildings.
       
        self.schools = [item for item in self.buildings if  item.type == 'school']
        self.workplaces = [item for item in self.buildings if item.type == 'market']

        self.roadNodes, self.roads = generateRoads_and_RoadNodesFromFile(self, 'RoadNodes.csv', 'Roads.csv')       
        self.vehicles = generateVehicles(self)
       
        # DictionaryList  = []
        # Index = []
        # for item in self.population:
        #     dict = {'familyId': item.familyId, 'homeId': item.homeId, 'schoolId': item.schoolId, 'workplaceId': item.workplaceId,  
        #             'age':item.age, 'sex': item.sex, 'infected':item.infected, 'infectionTime': item.infectionTime,
        #             'type': item.type, 'education': item.education, 'homeX': item.homeX, 'homeY':item.homeY}
        #     Index.append(item.id)
        #     DictionaryList.append(dict)
        # df = pd.DataFrame(DictionaryList, index = Index)
        # df.to_csv('Population.csv')
        

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

        self.simulate()
        
    def simulate(self):
        # plt.figure(figsize=(100, 100))      
        # for item in self.roadNodes:
        #     plt.scatter(item.x, item.y, s = 100, c = (0,1,0), alpha = 0.5)   

        # for road in self.roads:
        #     for i in range(len(road.nodes) - 1):
        #         plt.plot((road.nodes[i].x, road.nodes[i + 1].x), (road.nodes[i].y, road.nodes[i + 1].y), c = (0,0,1), alpha = 0.5)

        # for vehicl in self.vehicles:
        #     plt.scatter(vehicl.x, vehicl.y, marker='^',s = 50,  c = (0,1,1))

        # for vehicl in self.population:
        #     if vehicl.infected == True:
        #         plt.scatter(vehicl.x, vehicl.y, s = 1,  c = (1,0,0), alpha=1)
        # #     else:
        # #         plt.scatter(vehicl.x, vehicl.y, s = 1,  c = (1,1,0), alpha=1)

        # plt.title('Roads = Line , RodeNodes = Circle, Vehicles= Red Triangle')    
        # plt.show()

        if (self.time - 25) % (7 * 24)  == 0:
            print("Not saturday, workday starts")
            for items in self.population:
                items.checked = False

        self.time += SIMULATION_TIME_STEP
        if self.time > 200:
            exit(0)
        updateAllVehicles(self)
        buildingInteraction(self)
        # states = []
        for entity in self.population:
            BT = behaviorTree[entity.type]
            # Change the state of entity and update as the output of BT processing.
            BT(self, entity)
            # states.append(entity)

        print("Time End:", self.time)
        infectedcount = 0
        outdict = {}
        Humansl = [{'infected': bool(item.infected), 'x': item.x, 'y': item.y} for item in self.population]        
        Vehiclel = [{'x': item.x, 'y': item.y, 'passengers': [ids.id for ids in item.passengers]} for item in self.vehicles]
        outdict = {'Human': Humansl, 'Vehicle':Vehiclel}
        for item in self.population:            
            if item.infected == True:
                item.infectionTime += 1
                if item.infectionTime > INFECTION_PERIOD:
                    item.infected = False
                    item.infectionTime = 0   
                infectedcount += 1
        
        print("Infected Count: ", infectedcount)
        # time.sleep(0.2)


        if self.time > 200:
            exit(0)

        else:
            with open('newlog/particlelog' +str(self.time) + '.json', 'w') as fp:
                json.dump(outdict, fp)
            self.simulate()

if __name__ == "__main__":
    w = World()
