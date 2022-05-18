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

    def __init__(self, 
        name: str = "", 
        ID: str = "", 
        layers: List[Layer] = [], 
        params: Params = Params(),
         ports: List[Port] = [], 
        entity: str = "",  
        xspan: int = -1, 
        yspan: int = -1, 
        xpos: float = -1, 
        ypos: float = -1
    ) -> None:
        """Creates a new Component object

        Args:
            json (dict, optional): json dict after json.loads(). Defaults to None.
            device_ref (Device, optional): pointer for the Device object. Defaults to None.

        Raises:
            Exception: [description]
        """
        self.name: str = name
        self.ID: str = ID
        self.params = params
        self.entity: str = entity
        self.xspan: int = xspan
        self.yspan: int = yspan
        self.ports: List[Port] = ports
        self.layers: List[Layer] = layers

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

    @staticmethod
    def from_parchmint_v1(json, device_ref=None):
        """Creates a new Component object from the json dict

        Args:
            json (dict): json dict after json.loads()
            device_ref (Device, optional): pointer for the Device object. Defaults to None.

        Returns:
            Component: component object
        """
        if device_ref is None:
            raise Exception(
                "Cannot Parse Component from JSON with no Device Reference, check device_ref parameter in constructor "
            )

        component = Component()
        
        component.name = json["name"]
        component.ID = json["id"]
        component.entity = json["entity"]
        component.xspan = json["x-span"]
        component.yspan = json["y-span"]
        component.params = Params(json["params"])
        component.layers = [device_ref.get_layer(layer_id) for layer_id in json["layers"]]

        for port in json["ports"]:
            component.ports.append(Port(port))

        if component.params:
            if component.params.exists("position"):
                component.xpos = component.params.get_param("position")[0]
                component.ypos = component.params.get_param("position")[1]

        return component


    @staticmethod
    def from_parchmint_v1_2(json, device_ref=None):
        """Creates a new Component object from the json dict"""
        return Component.from_parchmint_v1(json, device_ref)
