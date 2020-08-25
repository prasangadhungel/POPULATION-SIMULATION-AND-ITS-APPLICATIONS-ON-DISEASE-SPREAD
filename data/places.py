import sys
import random
import pandas as pd
sys.path.append("..")

from buildings import Building
from family import Family

from data.configuration import *

from numpy import vstack,array
from numpy.random import rand

        
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
