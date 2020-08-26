from typing import Optional
from parchmint.params import Params


class Layer:

    def __init__(self, json=None) -> None:
        self.id: Optional[str] = None
        self.name: Optional[str] = None
        self.type: Optional[str] = None
        self.params: Params = Params()

        if json:
            self.parse_from_json(json)

    def parse_from_json(self, json):
        self.name = json["name"]
        self.id = json["id"]
        self.type = json["type"]
        self.params = Params(json["params"])

    def to_parchmint_v1(self):
        return {
            "name": self.name,
            "id": self.id,
            "type": self.type,
            "params": self.params.to_parchmint_v1(),
        }

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
