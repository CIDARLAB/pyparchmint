from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from parchmint.device import Device

from typing import List, Tuple

import numpy as np

from parchmint.layer import Layer
from parchmint.params import Params
from parchmint.port import Port


class Component:
    """The component class describes all the components in the device."""

    def __init__(self, json_data=None, device_ref: Device = None):
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
        self._ports: List[Port] = []
        self.layers: List[Layer] = []

        if json_data is not None:
            if device_ref is None:
                raise Exception(
                    "Cannot Parse Component from JSON with no Device Reference, check device_ref parameter in constructor "
                )
            self.parse_from_json(json_data, device_ref)

    @property
    def ports(self) -> List[Port]:
        """Returns the ports of the component

        Returns:
            List[Port]: list of ports
        """
        return self._ports

    @property
    def component_spacing(self) -> float:
        """Returns the component spacing

        Returns:
            float: component spacing
        """
        return self.params.get_param("componentSpacing")

    @component_spacing.setter
    def component_spacing(self, value: float):
        """Sets the component spacing

        Args:
            value (float): component spacing
        """
        self.params.set_param("componentSpacing", value)

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

    @property
    def rotation(self) -> float:
        """Returns the rotation of the component

        Raises:
            KeyError: when no rotation parameter is found

        Returns:
            int: rotation of the component
        """
        try:
            return self.params.get_param("rotation")
        except Exception:
            print("Could not find rotation for component")
            raise KeyError

    @rotation.setter
    def rotation(self, value):
        """Sets the rotation of the component

        Args:
            value (int): rotation of the component
        """
        self.params.set_param("rotation", value)

    def add_component_ports(self, ports: List[Port]) -> None:
        """Adds component ports to the component

        Args:
            ports (List[Port]): list of port objects
        """
        for port in ports:
            self.add_component_port(port)

    def add_component_port(self, port: Port) -> None:
        """Adds a component port to the component

        Args:
            port (Port): port object
        """
        self._ports.append(port)

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
            self.add_component_port(Port(port))

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
        # Set the position parameter if it doesnt exist, set it to -1, -1
        if not self.params.exists("position"):
            self.params.set_param("position", [-1, -1])
        ret = {
            "name": self.name,
            "id": self.ID,
            "layers": [layer.ID for layer in self.layers],
            "params": self.params.to_parchmint_v1(),
            "ports": [p.to_parchmint_v1() for p in self._ports],
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
        for port in self._ports:
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

    def rotate_point(
        self, xpos: float, ypos: float, angle: float
    ) -> Tuple[float, float]:
        """Rotates a point around the topleft corner of the component clockwise

        Args:
            xpos (float): x coordinate of the point
            ypos (float): y coordinate of the point
            angle (float): angle of rotation in degrees

        Returns:
            Tuple[float, float]: A tuple containing the rotated coordinates
        """
        # Setup the center to be used the translation matrices
        center_x = self.xspan / 2
        center_y = self.yspan / 2

        # Setup all the corner points
        old_topLeft = np.array((0, 0, 1)).transpose()
        old_topRight = np.array((self.xspan, 0, 1)).transpose()
        old_bottomLeft = np.array((0, self.yspan, 1)).transpose()
        old_bottomRight = np.array((self.xspan, self.yspan, 1)).transpose()

        pos = np.array(((xpos), (ypos), (1)))

        T1 = np.array(((1, 0, -center_x), (0, 1, -center_y), (0, 0, 1)))

        theta = np.radians(angle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
        T2 = np.array(((1, 0, center_x), (0, 1, center_y), (0, 0, 1)))

        # Rotate the topRight corner and the bottomLeft corner about the center
        rotated_topLeft = T2.dot(R.dot(T1.dot(old_bottomLeft)))
        rotated_topRight = T2.dot(R.dot(T1.dot(old_topLeft)))
        rotated_bottomRight = T2.dot(R.dot(T1.dot(old_topRight)))
        rotated_bottomLeft = T2.dot(R.dot(T1.dot(old_bottomRight)))

        # Find the new position of the topleft corner by finding the min of all the corner points
        xmin = min(
            rotated_topLeft[0],
            rotated_topRight[0],
            rotated_bottomLeft[0],
            rotated_bottomRight[0],
        )
        ymin = min(
            rotated_topLeft[1],
            rotated_topRight[1],
            rotated_bottomLeft[1],
            rotated_bottomRight[1],
        )

        T3 = np.array(((1, 0, -xmin), (0, 1, -ymin), (0, 0, 1)))

        new_pos = T3.dot(T2.dot(R.dot(T1.dot(pos))))
        return (round(new_pos[0]), round(new_pos[1]))

    def rotate_point_around_center(
        self, xpos: float, ypos: float, angle: float
    ) -> Tuple[float, float]:
        """Rotates a point around the component center clockwise

        Args:
            xpos (float): x coordinate of the point
            ypos (float): y coordinate of the point
            angle (float): angle of rotation in degrees

        Returns:
            Tuple[float, float]: A tuple containing the rotated coordinates
        """
        # Setup the center to be used the translation matrices
        center_x = self.xpos + self.xspan / 2
        center_y = self.ypos + self.yspan / 2

        pos = np.array(((xpos), (ypos), (1)))

        T1 = np.array(((1, 0, -center_x), (0, 1, -center_y), (0, 0, 1)))

        theta = np.radians(angle)
        c, s = np.cos(theta), np.sin(theta)
        R = np.array(((c, -s, 0), (s, c, 0), (0, 0, 1)))
        T2 = np.array(((1, 0, center_x), (0, 1, center_y), (0, 0, 1)))

        new_pos = T2.dot(R.dot(T1.dot(pos)))
        return (round(new_pos[0]), round(new_pos[1]))

    def get_rotated_component_definition(self, angle: int) -> Component:
        """Returns a new component with the same parameters but rotated by the given angle

        Args:
            angle (int): angle of rotation

        Returns:
            Component: [description]
        """
        new_topLeft = self.rotate_point(0, 0, angle)
        new_topRight = self.rotate_point(self.xspan, 0, angle)
        new_bottomLeft = self.rotate_point(0, self.yspan, angle)
        new_bottomRight = self.rotate_point(self.xspan, self.yspan, angle)

        # Find xmin, ymin, xmax, ymax for all the corner points
        xmin = min(
            new_topLeft[0], new_topRight[0], new_bottomLeft[0], new_bottomRight[0]
        )
        ymin = min(
            new_topLeft[1], new_topRight[1], new_bottomLeft[1], new_bottomRight[1]
        )
        xmax = max(
            new_topLeft[0], new_topRight[0], new_bottomLeft[0], new_bottomRight[0]
        )
        ymax = max(
            new_topLeft[1], new_topRight[1], new_bottomLeft[1], new_bottomRight[1]
        )

        # Find the new xspan and yspan
        new_xspan = abs(xmax - xmin)
        new_yspan = abs(ymax - ymin)

        # Create a new component with the rotated coordinates
        rotated_component = Component()
        rotated_component.name = self.name
        rotated_component.ID = self.ID
        rotated_component.layers = self.layers
        rotated_component.params = self.params
        rotated_component.xpos = xmin
        rotated_component.ypos = ymin
        rotated_component.entity = self.entity

        # Add the x and y spans
        rotated_component.xspan = int(new_xspan)
        rotated_component.yspan = int(new_yspan)

        # Set the rotation angle to 0 to ensure that future operations don't mistake this to not have a rotation
        rotated_component.rotation = 0

        # Create new ports with new rotated coordinates
        for port in self._ports:
            new_port = Port()
            new_port.label = port.label
            new_location = self.rotate_point(port.x, port.y, angle)
            new_port.x = new_location[0]
            new_port.y = new_location[1]
            rotated_component.add_component_port(new_port)

        return rotated_component

    def rotate_component(self) -> None:
        """Returns a new component with the same parameters but rotated by the given angle

        Args:
            None

        Returns:
            None
        """

        # first rotate ports before everything gets confusion
        for port in self._ports:
            print(port.label, port.x, port.y)
            new_location = self.rotate_point(port.x, port.y, self.rotation)
            port.x = new_location[0]
            port.y = new_location[1]

        new_topLeft = self.rotate_point_around_center(
            self.xpos + 0, self.ypos + 0, self.rotation
        )
        new_topRight = self.rotate_point_around_center(
            self.xpos + self.xspan, self.ypos + 0, self.rotation
        )
        new_bottomLeft = self.rotate_point_around_center(
            self.xpos + 0, self.ypos + self.yspan, self.rotation
        )
        new_bottomRight = self.rotate_point_around_center(
            self.xpos + self.xspan, self.ypos + self.yspan, self.rotation
        )

        # Find xmin, ymin, xmax, ymax for all the corner points
        xmin = min(
            new_topLeft[0], new_topRight[0], new_bottomLeft[0], new_bottomRight[0]
        )
        ymin = min(
            new_topLeft[1], new_topRight[1], new_bottomLeft[1], new_bottomRight[1]
        )
        xmax = max(
            new_topLeft[0], new_topRight[0], new_bottomLeft[0], new_bottomRight[0]
        )
        ymax = max(
            new_topLeft[1], new_topRight[1], new_bottomLeft[1], new_bottomRight[1]
        )

        # Find the new xspan and yspan
        new_xspan = abs(xmax - xmin)
        new_yspan = abs(ymax - ymin)
        self.xspan = int(new_xspan)
        self.yspan = int(new_yspan)

        # Create a new component with the rotated coordinates
        self.xpos = xmin
        self.ypos = ymin
