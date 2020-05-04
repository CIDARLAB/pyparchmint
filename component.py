from .params import Params
from .port import Port

class Component:

    def __init__(self, json=None):
        self.name = None
        self.ID = None
        self.params = Params()
        self.entity = None
        self.xpos = None
        self.ypos = None
        self.xspan = None
        self.yspan = None
        self.ports = []
        self.layers = []

        if json:
            self.parseFromJSON(json)

    def parseFromJSON(self, json):
        self.name = json["name"]
        self.ID = json["id"]
        self.entity = json["entity"]
        self.xspan = json["xspan"]
        self.yspan = json["yspan"]
        self.params = Params(json["params"])
        self.layers = json["layers"]

        for port in json["ports"]:
            self.ports.append(Port(port))

        if self.params:
            self.xpos = self.params.getParam("position")[0]
            self.ypos = self.params.getParam("position")[1]

    def __str__(self):
            return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def toParchMintV1(self):
        data = {}
        data["name"] = self.name
        data["id"] = self.ID
        data["layers"] = self.layers
        data["params"] = self.params.toParchMintV1()
        data["ports"] = [p.toParchMintV1() for p in self.ports]
        data["entity"] = self.entity

        return data
    def __eq__(self, obj):
        if isinstance(obj, Component):
            return obj.ID == self.ID
        else:
            return False
