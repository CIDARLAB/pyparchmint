class Port:
    def __init__(self, json=None):
        """Creates a ComponentPort which is used to represent the points
        where a connection connects on the component

        Args:
            json (dict, optional): json dict. Defaults to None.
        """
        self.x: int = -1
        self.y: int = -1
        self.label: str = ""
        self.layer: str = ""

        if json:
            self.parse_from_json(json)

    def parse_from_json(self, json):
        """Parses the json dict from json.loads()

        Args:
            json ([dict): dictionary
        """
        self.x = json["x"]
        self.y = json["y"]
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
            "x": self.x,
            "y": self.y,
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
