from pyparchmint.layer import Layer
import networkx as nx

from .component import Component
from .connection import Connection


class Device:

    def __init__(self, json=None):
        self.name = ""
        self.components = []
        self.connections = []
        self.layers = []
        self.params = dict()
        self.features = [] # Store Raw JSON Objects for now
        self.G = nx.MultiDiGraph()
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
    
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return str(self.__dict__)
