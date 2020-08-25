from typing import Optional
from pyparchmint.params import Params

class Layer:

    def __init__(self, json = None) -> None:
        self.ID: Optional[str] = None
        self.name: Optional[str] = None
        self.type: Optional[str] = None
        self.params: Params = Params()

        if json:
            self.parseFromJSON(json)

    def parseFromJSON(self, json):
        self.name = json["name"]
        self.ID = json["id"]
        self.type = json["type"]
        self.params = Params(json["params"])


    def toParchMintV1(self):
        data = {}
        data["name"] = self.name
        data["id"] = self.ID
        data["type"] = self.type
        data["params"] = self.params.toParchMintV1()

        return data

    def __str__(self):
            return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)