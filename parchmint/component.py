from __future__ import annotations
from typing import List, Tuple
from parchmint.params import Params
from parchmint.port import Port
from parchmint.layer import Layer


class Component:
    def __init__(self, json=None, device_ref=None):
        self.name: str = ""
        self.ID: str = ""
        self.params = Params()
        self.entity: str = ""
        self.xpos: int = -1
        self.ypos: int = -1
        self.xspan: int = -1
        self.yspan: int = -1
        self.ports: List[Port] = []
        self.layers: List[Layer] = []

        if json is not None:
            if device_ref is None:
                raise Exception(
                    "Cannot Parse Component from JSON with no Device Reference, check device_ref parameter in constructor "
                )
            self.parse_from_json(json, device_ref)

    def add_component_ports(self, ports: List[Port]) -> None:
        for port in ports:
            self.ports.append(port)

    def parse_from_json(self, json, device_ref: Device = None):
        if device_ref is None:
            raise Exception(
                "Cannot Parse Component from JSON with no Device Reference, check device_ref parameter in constructor "
            )
        self.name = json["name"]
        self.ID = json["id"]
        self.entity = json["entity"]
        self.xspan = json["x-span"]
        self.yspan = json["y-span"]
        self.params = Params(json["params"])
        self.layers = [device_ref.get_layer(layer_id) for layer_id in json["layers"]]

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
            "layers": [layer.ID for layer in self.layers],
            "params": self.params.to_parchmint_v1(),
            "ports": [p.to_parchmint_v1() for p in self.ports],
            "entity": self.entity,
            "x-span": int(self.xspan),
            "y-span": int(self.yspan),
        }

    def __eq__(self, obj):
        if isinstance(obj, Component):
            return obj.ID == self.ID
        else:
            return False

    def get_port(self, label: str) -> Port:
        for port in self.ports:
            if label == port.label:
                return port
        raise Exception("Could not find port with the label: {}".format(label))

    def get_absolute_port_coordinates(self, port_label: str) -> Tuple[float, float]:
        port = self.get_port(port_label)
        x = self.xpos + port.x
        y = self.ypos + port.y
        return (x, y)
