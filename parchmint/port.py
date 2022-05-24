class Port:
    """Describes the port on a component"""

    def __init__(self, json=None):
        """Creates a ComponentPort which is used to represent the points
        where a connection connects on the component

        Args:
            json (dict, optional): json dict. Defaults to None.
        """
        self.x: float = -1
        self.y: float = -1
        self.label: str = ""
        self.layer: str = ""

        if json:
            self.parse_from_json(json)

    @property
    def x(self) -> int:
        """Returns the x coordinate of the port"""
        return self._xpos

    @x.setter
    def x(self, value: int) -> None:
        """Sets the x coordinate of the port

        Args:
            value (int): x coordinate
        """
        self._xpos = value

    @property
    def y(self) -> int:
        """Returns the y coordinate of the port"""
        return self._ypos

    @y.setter
    def y(self, value: int) -> None:
        """Sets the y coordinate of the port

        Args:
            value (int): y coordinate
        """
        self._ypos = value

    def parse_from_json(self, json):
        """Parses the json dict from json.loads()

        Args:
            json ([dict): dictionary
        """
        self._xpos = json["x"]
        self._ypos = json["y"]
        self.label = json["label"]
        self.layer = json["layer"]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        return {
            "x": self._xpos,
            "y": self._ypos,
            "label": self.label,
            "layer": self.layer,
        }

    def __eq__(self, obj):
        if isinstance(obj, Port):
            return obj.label == self.label
        else:
            return False

    def __hash__(self) -> int:
        return hash(repr(self))
