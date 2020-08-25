from helpers import distance, findClosest
import random
import time
from data.configuration import VEHICLES
from road import RoadNode, Road
from vehicles import Vehicle
import pandas as pd

def assignVehicle(entity, vehicles):
    # for now assign the first vehicle in the list.
    minDist = 9000000000
    minId   = 0
    for vehicle in vehicles:
        dist = distance(entity, vehicle)
        if dist < minDist:
            minDist   = dist
            minId     = vehicle.id
    
    return minDist, minId

def assignMarket(nodeList, world): 
    ran = random.randint(0, len(nodeList) - 1)
    minDistance = 1000000000
    minId       = 0
    for item in world.visitables:
        dist = ((world.buildings[item].x - nodeList[ran].x)**2 + (world.buildings[item].y - nodeList[ran].y) ** 2) ** 0.5
        if dist < minDistance:
            minId = world.buildings[item].id
            minDistance = dist

    return minId


def assignSchool(nodeList, world): 
    ran = random.randint(0, len(nodeList) - 1)
    minDistance = 1000000000
    minId       = 0
    for item in world.schools:
        dist = ((item.x - nodeList[ran].x)**2 + (item.y - nodeList[ran].y) ** 2) ** 0.5
        if dist < minDistance:
            minId = item.id
            minDistance = dist

    return minId

def assignWorkPlace(nodeList, world): 
    ran = random.randint(0, len(nodeList) - 1)
    minDistance = 1000000000
    minId       = 0
    for item in world.workplaces:
        dist = ((item.x - nodeList[ran].x)**2 + (item.y - nodeList[ran].y) ** 2) ** 0.5
        if dist < minDistance:
            minId = item.id
            minDistance = dist

    return minId


def assignBuildings(world):
    for family in world.families:
        minDist = 100000000
        minCoord = []
        minId = 0
        for building in world.buildings:
            if building.special:
                continue
            dist = distance(building, family)
            if dist < minDist:
                minDist = dist
                minCoord = [building.x,building.y]
                minId = building.id
        # Assign family to coordinate.
        family.changeLocation(minCoord[0], minCoord[1])
        family.buildingId = minId
        for peopleID in family.occupants:
            world.buildings[minId - 1].addOccupant(world.population[peopleID - 1])
            world.population[peopleID - 1].homeId = minId

def assignBuildingsTypes(buildings):
    # Three types of buildings: Schools, hospitals and markets.
    # Take 30% of the buildings and convert them into markets. Then update their location.
    specials = [building.id for building in buildings if building.special]
    totalSpecial = len(specials)
    marketBuildingsSize = int( totalSpecial * 0.40 )
    marketBuildings = []
    for item in specials:
        if len(marketBuildings) != marketBuildingsSize:
            # mark this building as a market building.
            buildings[item -1].type = 'market';
            # Update the market array's each building as the average of the position.
            # Append this building id to marketbuildings
            marketBuildings.append(item)
            # Total sum of centers of all market buildings.
            totalX = 0 
            totalY = 0
            for building in marketBuildings:
                totalX += buildings[building].x
                totalY += buildings[building].y
            cX = totalX / len(marketBuildings)
            cY = totalY / len(marketBuildings)
            # Reset center for all market buildings to a common center.
            for building in marketBuildings:
                buildings[building].x = cX
                buildings[building].y = cY
    
    # Process for schools and hospitals now
    schoolsRequired = int(totalSpecial * 0.4)
    schools = []
    startIndex = int(totalSpecial*0.4) + 1
    index = startIndex

    while(len(schools) < schoolsRequired):
        buildings[specials[index]].type = "school"
        schools.append(specials[index])
        index += 1

    #Process for hospitals now.
    hospitals = []
    while(index < totalSpecial):
        buildings[specials[index - 1]].type = "hospital"
        hospitals.append(specials[index])
        index += 1

    print("Completed processing special buildings.")

def assignPeople(world, families):
    # Generate a list of schools and workplaces.
    # schools = [item for item in world.buildings if item.special is True and item.type is 'school']
    # workplaces = [item for item in world.buildings if item.special is True and item.type is 'market']
    for family in families:
        size = family.size
        if size > 2:
            # This family contains a child ?
            while size > 2:
                size -= 1
                # Allocate a child.
                world.population[family.occupants[size -1]].type = "student"
                world.population[family.occupants[size -1]].age = random.randint(5,16)
                me = world.population[family.occupants[size -1]]
                world.population[family.occupants[size -1]].schoolId = findClosest(me, world.schools)
                world.population[family.occupants[size - 1]].education = world.population[family.occupants[size -1]].age - 3

            me = world.population[family.occupants[size - 1] - 1]
            world.population[family.occupants[size - 1] - 1].type = "working"
            world.population[family.occupants[size - 1] - 1].age = random.randint(30, 50)
            world.population[family.occupants[size - 1] - 1].sex = "Male"
            world.population[family.occupants[size - 1] - 1].education = random.randint(10, 16)
            me.workplaceId = findClosest(me, world.workplaces)

            me = world.population[family.occupants[size - 2] - 1]
            world.population[family.occupants[size - 2] - 1].type = "working"
            world.population[family.occupants[size - 2] - 1].age = world.population[family.occupants[size-1]].age
            world.population[family.occupants[size - 2] - 1].sex = "Female"
            world.population[family.occupants[size - 2] - 1].education = random.randint(7, 15)
            me.workplaceId = findClosest(me, world.workplaces)


        else:
            me = world.population[family.occupants[0] - 1]
            world.population[family.occupants[0] - 1].age = random.randint(30, 50)
            world.population[family.occupants[0] - 1].sex = "Male"
            world.population[family.occupants[0] - 1].type = "working"
            me.workplaceId = findClosest(me, world.workplaces)

            me = world.population[family.occupants[1] - 1]
            world.population[family.occupants[1] - 1].age = world.population[family.occupants[0] - 1].age - 2
            world.population[family.occupants[1] - 1].sex = "Female"
            world.population[family.occupants[1] - 1].type = "working"
            me.workplaceId = findClosest(me, world.workplaces)

    print("Completed assigning attributes to each family.")

def generateRoadNodes(world):
    """
    """
    nodes = []
    # Push special buildings as nodes.
    for item in world.visitables:
        # Pull a special building from the world.
        building = world.buildings[item - 1]
        n = RoadNode(id = len(nodes)+1, x=building.x, y=building.y)
        nodes.append(n)

    # Append 10-50 random nodes into the network.
    for _ in range(random.randint(40, 50)):
        n = RoadNode(id= len(nodes) +1, x = random.random() * MAP_MAX_X, y = random.random() * MAP_MAX_Y)
        nodes.append(n)
    return nodes


def generateRoads_and_RoadNodes(world):
    roads=[]
    roadNodes=[]
    print("World visitables:", len(world.visitables)) 
    for item in world.visitables:
        building = world.buildings[item - 1]
        n = RoadNode(id = len(roadNodes) + 1, x=building.x, y=building.y)
        roadNodes.append(n)

    for _ in range(MAP_ROADS_COUNT):
        max_nodes = random.randint(8, 12)
        tempNode  = roadNodes[:]
        firstNode = tempNode[random.randint(0,len(tempNode)-1)]
        firstNode.connected = True
        road = [firstNode]

        for _ in range(max_nodes):
            minDist = 1000000
            nextNode = []

            tempNode.remove(firstNode)
            if len(tempNode) < 1:
                break

            for node in tempNode:  
                dist=distance(node, firstNode)
                if dist < minDist:
                    nextNode = node
                    minDist= dist
            nextNode.connected = True
            road.append(nextNode)
            firstNode = nextNode
        
        
        roads.append(Road(roadNodeList = road, id = len(roads) + 1))
    
    for nod in roadNodes:
        if nod.connected == False:
            for _ in range(MAP_ROADS_COUNT):
                max_nodes = random.randint(4, 8)
                tempNode  = roadNodes[:]
                firstNode = nod
                firstNode.connected = True
                road = [firstNode]

                for _ in range(max_nodes):
                    minDist = 1000000
                    nextNode = []

                    tempNode.remove(firstNode)
                    if len(tempNode) < 1:
                        break

                    for node in tempNode:  
                        dist=distance(node, firstNode)
                        if dist < minDist:
                            nextNode = node
                            minDist= dist
                    nextNode.connected = True
                    road.append(nextNode)
                    firstNode = nextNode
                
                # if len(road) > 0:
                #     road.append(road[0])
                
                roads.append(Road(roadNodeList = road, id = len(roads) + 1))
            
    # plt.show()    
    return roadNodes, roads


def generateRoads_and_RoadNodesFromFile(world, nodesFile, roadFile):
    roads = {}
    roadNodes={}
    dfnode = pd.read_csv(nodesFile)
    dfroad = pd.read_csv(roadFile)
    # plt.figure(figsize=(50, 50)) 
    for i in range(len(dfnode)):
        roadNodes[dfnode.iloc[i, 0]] = RoadNode(id = dfnode.iloc[i, 0], x = dfnode.loc[i, 'x'], y = dfnode.loc[i, 'y'])
        # plt.scatter(dfnode.loc[i, 'x'], dfnode.loc[i, 'y'],s = 50, c = (0,1,0))

    # roadcount = 0
    for i in range(len(dfroad)):
        if len([roadNodes[abc] for abc in [int(item) for item in dfroad.loc[i, 'nodes'].strip('[]').split(', ')] ]) > 25:
            # roadcount += 1
            roads[dfroad.iloc[i,0]] = Road(roadNodeList = [roadNodes[abc] for abc in [int(item) for item in dfroad.loc[i, 'nodes'].strip('[]').split(', ')] ],
                              id = dfroad.iloc[i,0])
    # print(roadcount)
    # exit(0)
    return roads        



def generateVehicles(world):
    vehicles = []
    for i in range(VEHICLES):
        randomroadID =  random.choice(list(world.roads.keys()))
        vehicle    = Vehicle(world, id = i + 1, roadId = randomroadID)
        world.roads[randomroadID].hasVehicle = True
        vehicles.append(vehicle)
        # plt.scatter(vehicle.x, vehicle.y, marker='^',s = 75,  c = (1,0,0))
    
    for road in world.roads:
        if world.roads[road].hasVehicle == False and len(world.roads[road].nodes) > 60:
            vehicle    = Vehicle(world, id = len(vehicles) + 1, roadId = world.roads[road].id)
            world.roads[road].hasVehicle = True
            vehicles.append(vehicle)
    #         plt.scatter(vehicle.x, vehicle.y, marker='^',s = 75,  c = (1,0,0))
    
    # plt.title('Roads = Line , RodeNodes = Circle, Vehicles at start= Red Triangle')
    # plt.show()
    
    # plt.savefig('image/0.png')
    return vehicles
