from pyparchmint.layer import Layer
import networkx as nx
from typing import Optional
from .component import Component
from .connection import Connection
from .params import Params


class Device:

    def __init__(self, json=None):
        self.name = ""
        self.components = []
        self.connections = []
        self.layers = []
        self.params = Params()
        self.features = [] # Store Raw JSON Objects for now
        self.xspan = None
        self.yspan = None
        self.G = nx.MultiGraph()

        if json:
            self.parseFromJSON(json)
            self.generateNetwork()

    def addComponent(self, component):
        if isinstance(component, Component):
            #Check if Component Exists, if it does ignore it
            if self.doesComponentExist(component):
                print("Component {} already present in device, hence skipping the component".format(component.name))
            
            self.components.append(component)

    def addConnection(self, connection):
        if isinstance(connection, Connection):
            self.connections.append(connection)
    
    def addLayer(self, layer):
        if isinstance(layer, Layer):
            self.layers.append(layer)

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
            
        for layer in json["layers"]:
            self.addLayer(Layer(layer))
    
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

    def doesComponentExist(self, component):
        return (component in self.components)
    
    def componentExists(self, componentid:str)->bool:
        for component in self.components:
            if componentid == component.ID:
                return component
        
        return False

    def connectionExists(self, connectionid:str)->bool:
        for connection in self.connections:
            if connectionid == self.connections:
                return connection
        
        return False

    def getComponent(self, id:str) -> Optional[Component]:
        if self.componentExists(id):
            for component in self.components:
                if component.ID == id:
                    return component

    def getConnection(self, id:str) -> Optional[Connection]:
        if self.connectionExists(id):
            for connection in self.connections:
                if connection.ID == id:
                    return connection

    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)

    def toParchMintV1(self):
        data = {}

        data["name"] = self.name
        data["components"] = [c.toParchMintV1() for c in self.components]
        data["connections"] = [c.toParchMintV1() for c in self.connections]
        data["params"] = self.params.toParchMintV1()
        data["version"] = 1
        data["layers"] = [layer.toParchMintV1() for layer in self.layers]

        return data

