from .params import Params

class Layer:

    def __init__(self, json = None) -> None:
        self.ID = None
        self.name = None
        self.type = None
        self.params = dict()

        if json:
            self.parseFromJSON(json)

    def parseFromJSON(self, json):
        self.name = json["name"]
        self.ID = json["id"]
        self.type = json["type"]

        self.params = Params(json["params"])

    def __str__(self):
            return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)