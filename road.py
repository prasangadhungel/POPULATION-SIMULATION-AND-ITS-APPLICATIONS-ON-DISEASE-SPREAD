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
        self.NodesList = []
        for node in self.nodes:
            self.NodesList.append(Node(node))
        
        for i in range(len(self.NodesList) - 1):
            self.NodesList[i].next = self.NodesList[i + 1]
            self.NodesList[i + 1].prev = self.NodesList[i]
