import random 
from helpers import * 
from assignment import *
# import time

def minDistance(entity, entityList):
    minDistance = 100000000
    retID = 0
    for x in entityList:
        a = distance(entity, x) 
        if(a < minDistance):
            minDistance = a
            retID = x.ID
    return retID

def simulateWorking(world, entity):
    if entity.reachedDestination == True and entity.destination.special == True:
        entity.destinationTime += 1
        if  entity.destinationTime > entity.destination.interaction_time and entity.isDelegated == False:
            print("Finished work, returning home")
            # time.sleep(0.1)
            vehicleDist, vehicleId = assignVehicle(entity, world.vehicles)
            if vehicleDist < 50:
                entity.reachedDestination = False
                entity.destinationTime = 0
                print("Passenger added in", vehicleId, "at:", world.time, " for returning home")                        
                entity.destination = world.buildings[entity.homeId - 1]
                world.vehicles[vehicleId - 1].addPassenger(entity)                        
                entity.isDelegated = True
                entity.delegator = vehicleId

    if (world.time//24) % 7 == 0:
        # Saturday

        if entity.atHome() and entity.isDelegated == False:
            # Entity is at home and hasn't travelled
            # entity.checked = True
            goesOut = flip(0.3)
            if goesOut  and world.time % 24 < 11:
                if entity.ownsVehicle:
                    vehicleId = entity.vehicleID
                    entity.isDelegated = True
                    entity.delegator = vehicleId
                else:
                    vehicleDist, vehicleId = assignVehicle(entity, world.vehicles)
                    # print(vehicleDist, entity.x, entity.y, world.vehicles[vehicleId - 1].x, world.vehicles[vehicleId - 1].y)
                    if vehicleDist < 50:
                        MarketID = assignMarket(world.roads[world.vehicles[vehicleId -1].roadId - 1].nodes, world)
                        # print("MarketID and VehicleID: ", MarketID, vehicleId)
                        entity.destination = world.buildings[MarketID - 1]
                        world.vehicles[vehicleId - 1].addPassenger(entity)
                        # print("Passenger added in", vehicleId, "at:", world.time, " enjoying holiday")      
                        # time.sleep(0.5)                  
                        entity.isDelegated = True
                        entity.delegator = vehicleId
            
            
        else:
            pass
            
    else:
        #not saturday
        if entity.type == "student" and entity.isDelegated == False and world.time % 24 > 1 and world.time % 24 < 8 and random.random() < 0.8:
            # student go to school
            vehicleDist, vehicleId = assignVehicle(entity, world.vehicles)
            if vehicleDist < 50:
                SchoolID = assignSchool(world.roads[world.vehicles[vehicleId -1].roadId - 1].nodes, world)
                entity.destination = world.buildings[SchoolID - 1]
                # print("SchoolID and VehicleID: ", SchoolID, vehicleId)
                print("Passenger added in", vehicleId, "at:", world.time, " for school")                                        
                world.vehicles[vehicleId - 1].addPassenger(entity)                        
                entity.isDelegated = True
                entity.delegator = vehicleId

        elif entity.type == "working" and entity.isDelegated == False  and  world.time % 24 < 8 and random.random() < 0.8:
            # student go to school
            vehicleDist, vehicleId = assignVehicle(entity, world.vehicles)
            if vehicleDist < 50:
                WorkPlaceID = assignWorkPlace(world.roads[world.vehicles[vehicleId -1].roadId - 1].nodes, world)
                # print("WorkPlace and VehicleID: ", WorkPlaceID, vehicleId)
                print("Passenger added in", vehicleId, "at:", world.time, " for work")                        
                entity.destination = world.buildings[WorkPlaceID - 1]
                world.vehicles[vehicleId - 1].addPassenger(entity)                        
                entity.isDelegated = True
                entity.delegator = vehicleId

    

behaviorTree = {
    "student": simulateWorking,
    "working": simulateWorking
}