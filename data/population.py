import sys
sys.path.append("..")

from humans import *
from family import *
from data.configuration import *
import pandas as pd

def generatePopulation(world):
    population = []
    families   = []
    for i in range(FAMILIES):
        familySize = random.randint(2, 5)
        x = random.random() * MAP_MAX_X
        y = random.random() * MAP_MAX_Y
        fam = Family(world, size = familySize, id=len(families)+1, x = x, y = y)
        occupants = []
        while (familySize > 0):
            h = Human(
                world,
                age = 0,
                id  = len(population) + 1,
                infected = False,
                familyId = i,
                x = x,
                y = y,
                education = 0,
            )
            occupants.append(h.id)
            familySize -= 1            
            population.append(h)
        fam.setOccupants(occupants)
        families.append(fam)
    return (population, families)

def generatePopulationfromFile(world, filename):
    population  = []
    df = pd.read_csv(filename)
    for i in range(len(df)):
        population.append(Human(world, 
                                age = df.loc[i, 'age'],
                                id = i + 1,
                                education = df.loc[i, 'education'],
                                type = df.loc[i, 'type'],
                                infected = df.loc[i, 'infected'],
                                infectionTime = df.loc[i, 'infectionTime'],
                                familyId = df.loc[i, 'familyId'],
                                homeX = df.loc[i, 'homeX'],
                                homeY = df.loc[i, 'homeY'],
                                homeId = df.loc[i, 'homeId'],
                                susceptibility = df.loc[i, 'susceptibility'] / 5 ))
    
    
    return population