import sys
import random
import pandas as pd
sys.path.append("..")

from buildings import Building
from family import Family

from data.configuration import *

from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

def generateBuildings(world):
    locations = []
    for family in world.families:
        locations.append([family.x, family.y])

    buildings  = []
    toGen = len(world.families) / 4
    print(toGen)
    centroids, _ = kmeans(locations, toGen)
    for coord in centroids:
        isSpecial = random.random() < 0.10
        building = ()
        if not isSpecial:
            building = Building(world, id = len(buildings)+1, x=coord[0], y=coord[1])
        else:
            building = Building(world, special = True, id = len(buildings)+1, x=coord[0], y=coord[1], interaction_time=random.randint(3, 6))
        buildings.append(building)
    return buildings
        
def generateBuildingsfromFile(world, filename):
    buildings  = {}
    df = pd.read_csv(filename)
    for i in range(len(df)):
        building = Building(world, 
                        id = df.iloc[i,0],
                        type = df.loc[i, 'type'],
                        x = df.loc[i, 'x'],
                        y = df.loc[i, 'y'], 
                        interaction_time = df.loc[i, 'interaction_time'],
                        special = df.loc[i, 'special'])

        buildings[df.iloc[i,0]] = building
    return buildings
