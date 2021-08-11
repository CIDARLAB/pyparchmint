from typing import Optional


class Target:
    def __init__(self, json=None):
        """Creates a Target object that describes where the connection will connect to

        Args:
            json (dict, optional): json dict from json.loads(). Defaults to None.
        """
        self._component = ""
        self._port: Optional[str] = None

        if json:
            self.parse_from_json(json)

    def parse_from_json(self, json):
        """Loads the instance data from the json dict

        Args:
            json ([type]): json dict from json.loads()
        """
        self._component = json["component"]
        self._port = json["port"]

    @property
    def component(self) -> str:
        """Returns the component in the Target

        Returns:
            str: Target component ID
        """
        return self._component

    @component.setter
    def component(self, value: str) -> None:
        """Sets the component in the target

        Args:
            value (str): component ID
        """
        self._component = value

    @property
    def port(self) -> Optional[str]:
        """Returns the port label in the target

        Returns:
            Optional[str]: port label of the target
        """
        return self._port

    @port.setter
    def port(self, value: Optional[str]) -> None:
        """Sets the port in the target

        Args:
            value (str): port label for the given component
        """
        self._port = value

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self) -> dict:
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        return {
            "component": self._component,
            "port": self._port,
        }

    def __eq__(self, obj):
        if isinstance(obj, Target):
            return obj.component == self.component and obj.port == self.port
        else:
            return False

    def __hash__(self) -> int:
        return hash(repr(self))
