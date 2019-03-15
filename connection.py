from .params import Params
from .target import Target

class Connection:

    def __init__(self, json):

        self.name = None
        self.ID = None
        self.params = dict()
        self.source = None
        self.sinks = []

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