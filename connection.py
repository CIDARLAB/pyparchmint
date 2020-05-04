from .params import Params
from .target import Target

class Connection:

    def __init__(self, json=None):

        self.name = None
        self.ID = None
        self.entity = None
        self.params = Params()
        self.source = None
        self.sinks = []
        self.layer = None

        if json:
            self.parseFromJSON(json)

    def parseFromJSON(self, json):
        self.name = json["name"]
        self.ID = json["id"]
        self.params = Params(json["params"])

        self.source = Target(json["source"])

        for target in json["sinks"]:
            self.sinks.append(Target(target))

    def __str__(self):
            return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def toParchMintV1(self):
        data = {}
        
        data["sinks"] = [s.toParchMintV1() for s in self.sinks]
        data["name"] = self.name
        data["id"] = self.ID
        data["source"] = self.source.toParchMintV1()
        data["params"] = self.params.toParchMintV1()

        return data
