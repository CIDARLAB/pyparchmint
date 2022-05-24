from typing import Optional

from parchmint.params import Params


class Layer:
    """Layer Object

    Used to define a layer object that can be used in the device model.
    """

    def __init__(self, json_data=None) -> None:
        """Creates a new instance Layer

        Args:
            json (dict, optional): json dict after json.loads(). Defaults to None.
        """
        self._id: str = ""
        self.name: str = ""
        self.type: str = ""
        self.group: str = ""
        self.params: Params = Params()

        if json_data:
            self.parse_from_json(json_data)

    @property
    def ID(self) -> str:
        """Returns the ID of the layer

        Raises:
            ValueError: if ID is not set

        Returns:
            str: ID of the layer
        """
        return self._id

    @ID.setter
    def ID(self, value: str) -> None:
        """Sets the id of the layer

        Args:
            value (str): id of the layer
        """
        self._id = value

    def parse_from_json(self, json_data):
        """Loads instance data json dict from json.loads()

        Args:
            json ([type]): [description]
        """
        self.name = json_data["name"]
        self.ID = json_data["id"]
        self.type = json_data["type"]
        self.group = json_data["group"]
        self.params = Params(json_data["params"])

    def to_parchmint_v1(self):
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        return {
            "name": self.name,
            "id": self.ID,
            "type": self.type,
            "params": self.params.to_parchmint_v1(),
            "group": self.group,
        }

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def __hash__(self) -> int:
        return hash(repr(self))

    def __eq__(self, object_to_compare: object) -> bool:
        if isinstance(object_to_compare, Layer):
            return object_to_compare.ID == self.ID
        else:
            return False
