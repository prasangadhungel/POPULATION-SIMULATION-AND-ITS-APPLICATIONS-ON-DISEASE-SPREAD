# from buildings import *
import random

class Node(object):
    """
    linked List  Node
    """
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class RoadNode(object):
    """
        id, x, y.
    """
    def __init__(self,**kwargs):
        self.id = kwargs["id"]
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.connected = False
        self.roadIds = [0]
    

class Road(object):
    """
    """
    def __init__(self, **kwargs):
        self.nodes = kwargs["roadNodeList"]
        self.id = kwargs["id"]
        self.hasVehicle = False
        NodesList = []
        for node in self.nodes:
            NodesList.append(Node(node))
        
        for i in range(len(NodesList) - 1):
            NodesList[i].next = NodesList[i + 1]
            NodesList[i + 1].prev = NodesList[i]

        self.currentNode = NodesList[random.randint(0, len(NodesList) -1)]