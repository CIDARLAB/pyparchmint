from typing import Optional

from parchmint.params import Params


class Layer:
    def __init__(self, json=None) -> None:
        """Creates a new instance Layer

        Args:
            json (dict, optional): json dict after json.loads(). Defaults to None.
        """
        self.ID: Optional[str] = None
        self.name: Optional[str] = None
        self.type: Optional[str] = None
        self.group: str = ""
        self.params: Params = Params()

        if json:
            self.parse_from_json(json)

    def parse_from_json(self, json):
        """Loads instance data json dict from json.loads()

        Args:
            json ([type]): [description]
        """
        self.name = json["name"]
        self.ID = json["id"]
        self.type = json["type"]
        self.group = json["group"]
        self.params = Params(json["params"])

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

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Layer):
            return o.ID == self.ID
        else:
            return False
