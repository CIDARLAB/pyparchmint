from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parchmint.device import Device

from typing import List, Tuple

from parchmint.layer import Layer
from parchmint.params import Params
from parchmint.port import Port


class Component:
    """The component class describes all the components in the device."""

    def __init__(self, json=None, device_ref: Device = None):
        """Creates a new Component object

        Args:
            json (dict, optional): json dict after json.loads(). Defaults to None.
            device_ref (Device, optional): pointer for the Device object. Defaults to None.

        Raises:
            Exception: [description]
        """
        self.name: str = ""
        self.ID: str = ""
        self.params = Params()
        self.entity: str = ""
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

    @property
    def xpos(self) -> int:
        """returns the x coordinate of the component

        Raises:
            KeyError: when no position parameter object is found for the parchmint object

        Returns:
            int: x-coordinate
        """
        try:
            return self.params.get_param("position")[0]
        except Exception:
            print("Could not find xpos for component")
            raise KeyError

    @xpos.setter
    def xpos(self, value) -> None:
        """Sets the x-coordinate for the component

        Args:
            value (int): x coordianate of the object
        """
        if self.params.exists("position"):
            pos = self.params.get_param("position")
            pos[0] = value
            self.params.set_param("position", pos)
        else:
            self.params.set_param("position", [value, -1])

    @property
    def ypos(self) -> int:
        """Returns the y-coordinate in the parchmint object

        Raises:
            KeyError: When no position parameter is found in the parchmint object

        Returns:
            int: y coordinate of the component
        """
        try:
            return self.params.get_param("position")[1]
        except Exception:
            print("Could not find xpos for component")
            raise KeyError

    @ypos.setter
    def ypos(self, value) -> None:
        """Sets the y-coordinate of the component

        Args:
            value (int): y coordinate
        """
        if self.params.exists("position"):
            pos = self.params.get_param("position")
            pos[1] = value
            self.params.set_param("position", pos)
        else:
            self.params.set_param("position", [-1, value])

    def add_component_ports(self, ports: List[Port]) -> None:
        """Adds component ports to the component

        Args:
            ports (List[Port]): list of port objects
        """
        for port in ports:
            self.ports.append(port)

    def parse_from_json(self, json, device_ref=None):
        """Parses from the json dict

        Args:
            json (dict): json dict after json.loads()
        """
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
            if self.params.exists("position"):
                self.xpos = self.params.get_param("position")[0]
                self.ypos = self.params.get_param("position")[1]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        ret = {
            "name": self.name,
            "id": self.ID,
            "layers": [layer.ID for layer in self.layers],
            "params": self.params.to_parchmint_v1(),
            "ports": [p.to_parchmint_v1() for p in self.ports],
            "entity": self.entity,
            "x-span": int(self.xspan),
            "y-span": int(self.yspan),
        }

        return ret

    def __eq__(self, obj):
        if isinstance(obj, Component):
            return obj.ID == self.ID
        else:
            return False

    def get_port(self, label: str) -> Port:
        """Returns a port in the component identified by the corresponding label

        Args:
            label (str): label of the componentport

        Raises:
            Exception: if there is no component port with the corresponding label is found

        Returns:
            Port: component port
        """
        for port in self.ports:
            if label == port.label:
                return port
        raise Exception("Could not find port with the label: {}".format(label))

    def get_absolute_port_coordinates(self, port_label: str) -> Tuple[float, float]:
        """Gets the absolute coordinates of the component port identified by the label

        Args:
            port_label (str): unique identifier for the component port

        Returns:
            Tuple[float, float]: coordinates of the component port
        """
        port = self.get_port(port_label)
        x = self.xpos + port.x
        y = self.ypos + port.y
        return (x, y)

    def __hash__(self) -> int:
        return hash(repr(self))
