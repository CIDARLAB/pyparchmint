from typing import Dict, Optional

from parchmint.params import Params


class Layer:
    """Layer Object

    Used to define a layer object that can be used in the device model.
    """

    def __init__(
        self,
        layer_id: Optional[str] = None,
        name: Optional[str] = None,
        layer_type: Optional[str] = None,
        group: Optional[str] = None,
        params: Optional[Params] = None,
        json_data: Optional[Dict] = None,
    ) -> None:
        """Creates a new instance Layer

        Args:
            json (dict, optional): json dict after json.loads(). Defaults to None.
        """
        self._id: str = "" if layer_id is None else layer_id
        self.name: str = "" if name is None else name
        self.layertype: str = "" if layer_type is None else layer_type
        self.group: str = "" if group is None else group
        self.params: Params = Params() if params is None else params

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

    @property
    def layer_type(self) -> str:
        """Returns the layer type

        Returns:
            str: layer type
        """
        return self.layertype

    @layer_type.setter
    def layer_type(self, value: str) -> None:
        """Sets the layer type

        Args:
            value (str): layer type
        """
        self.layertype = value

    def parse_from_json(self, json_data):
        """Loads instance data json dict from json.loads()

        Args:
            json ([type]): [description]
        """
        self.name = json_data["name"]
        self.ID = json_data["id"]
        self.layertype = json_data["type"]
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
            "type": self.layertype,
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
