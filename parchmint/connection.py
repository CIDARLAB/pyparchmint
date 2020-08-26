from typing import Optional
from parchmint.params import Params
from parchmint.target import Target


class Connection:

    def __init__(self, json=None):

        self.name = None
        self.ID = None
        self.entity = None
        self.params = Params()
        self.source = None
        self.sinks = []
        self.layer: Optional[str] = None

        if json:
            self.parse_from_json(json)

    def parse_from_json(self, json):
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

    def to_parchmint_v1(self):
        return {
            "sinks": [s.to_parchmint_v1() for s in self.sinks],
            "name": self.name,
            "id": self.ID,
            "source": self.source.to_parchmint_v1(),
            "params": self.params.to_parchmint_v1(),
            "layer": self.layer,
        }