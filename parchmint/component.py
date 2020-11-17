from typing import Optional, List
from parchmint.params import Params
from parchmint.port import Port
from parchmint.layer import Layer

class Component:

    def __init__(self, json=None):
        self.name: Optional[str] = None
        self.ID: Optional[str] = None
        self.params = Params()
        self.entity: Optional[str] = None
        self.xpos: Optional[int] = None
        self.ypos: Optional[int] = None
        self.xspan: Optional[int] = None
        self.yspan: Optional[int] = None
        self.ports: List[Port] = []
        self.layers: List[Layer] = []

        if json:
            self.parse_from_json(json)

    def add_component_ports(self, ports:List[Port]) -> None:
        for port in ports:
            self.ports.append(port)

    def parse_from_json(self, json):
        self.name = json["name"]
        self.ID = json["id"]
        self.entity = json["entity"]
        self.xspan = json["x-span"]
        self.yspan = json["y-span"]
        self.params = Params(json["params"])
        self.layers = json["layers"]

        for port in json["ports"]:
            self.ports.append(Port(port))

        if self.params:
            self.xpos = self.params.get_param("position")[0]
            self.ypos = self.params.get_param("position")[1]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
        return {
            "name": self.name,
            "id": self.ID,
            "layers": self.layers,
            "params": self.params.to_parchmint_v1(),
            "ports": [p.to_parchmint_v1() for p in self.ports],
            "entity": self.entity,
            "x-span": self.xspan,
            "y-span": self.yspan,
        }

    def __eq__(self, obj):
        if isinstance(obj, Component):
            return obj.ID == self.ID
        else:
            return False
