import networkx as nx

from .component import Component
from .connection import Connection
from .params import Params


class Device:

    def __init__(self, json):
        self.name = ""
        self.components = []
        self.connections = []
        self.layers = []
        self.params = dict()
        self.features = [] # Store Raw JSON Objects for now
        self.xspan = None
        self.yspan = None
        self.G = nx.MultiGraph()

        if json:
            self.parseFromJSON(json)
            self.generateNetwork()
    

    def addComponent(self, component):
        if isinstance(component, Component):
            self.components.append(component)

    def addConnection(self, connection):
        if isinstance(connection, Connection):
            self.connections.append(connection)

    def parseFromJSON(self, json):
        self.name = json["name"]

        #Loop through the components
        for component in json["components"]:
            self.addComponent(Component(component))

        for connection in json["connections"]:
            self.addConnection(Connection(connection))

        if "params" in json.keys():
            self.params = Params(json["params"])

            if self.params.exists("xspan"):
                self.xspan = self.params.getParam("xspan")
            elif self.params.exists("width"):
                self.xspan = self.params.getParam("width")

            if self.params.exists("yspan"):
                self.yspan = self.params.getParam("yspan")
            elif self.params.exists("length"):
                self.yspan = self.params.getParam("length")
            
    def getComponents(self):
        return self.components
    
    def getConnections(self):
        return self.connections

    def generateNetwork(self):
        for component in self.components:
            self.G.add_node(component.ID)
        
        for connection in self.connections:
            sourceref = connection.source.component
            for sink in connection.sinks:
                sinkref = sink.component
                self.G.add_edge(sourceref, sinkref, source_port=connection.source, sink_port=sink)

    def getNameForID(self, id):
        for component in self.components:
            if component.ID == id:
                return component.name
    
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)
