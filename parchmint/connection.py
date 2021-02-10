from __future__ import annotations
from parchmint.layer import Layer
from typing import List, Optional, Tuple
from parchmint.params import Params
from parchmint.target import Target


class ConnectionPath:
    def __init__(
        self,
        source: Target = None,
        sink: Target = None,
        waypoints: List[Tuple[int, int]] = [],
        json=None,
    ) -> None:
        """Creates a new connection path object

        Args:
            source (Target): source corresponding to the path
            sink (Target): sink corresponding to the path
            waypoints (List[Tuple[int, int]], optional): list of the coordinates. Defaults to [].
        """
        super().__init__()
        self.__source: Target = source
        self.__sink: Target = sink
        self.__waypoints: List[Tuple[int, int]] = waypoints

        if json is not None:
            self.parse_parchmint_v1(json)

    @property
    def source(self) -> Target:
        return self.__source

    @property
    def sink(self) -> Target:
        return self.__sink

    @property
    def waypoints(self) -> List[Tuple[int, int]]:
        return self.__waypoints

    @waypoints.setter
    def waypoints(self, value: List[Tuple[int, int]]):
        self.__waypoints = value

    def to_parchmint_v1(self):
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        return {
            "source": None
            if self.__source is None
            else self.__source.to_parchmint_v1(),
            "sink": None if self.__sink is None else self.__sink.to_parchmint_v1(),
            "wayPoints": [list(wp) for wp in self.__waypoints],
        }

    def parse_parchmint_v1(self, json) -> None:
        self.__source = Target(json=json["source"])
        self.__sink = Target(json=json["sink"])
        self.__waypoints = [(wp[0], wp[1]) for wp in json["wayPoints"]]


class Connection:
    def __init__(self, json=None, device_ref=None):
        """[summary]

        Args:
            json ([type], optional): [description]. Defaults to None.
            device_ref ([type], optional): [description]. Defaults to None.

        Raises:
            Exception: [description]
        """
        self.name: Optional[str] = None
        self.ID: str = ""
        self.entity: Optional[str] = None
        self.params: Params = Params()
        self.source: Optional[Target] = None
        self.sinks: List[Target] = []
        self.layer: Layer = None
        self._paths: List[ConnectionPath] = []

        if json:
            if device_ref is None:
                raise Exception(
                    "Cannot Parse Connection from JSON with no Device Reference, check device_ref parameter in constructor "
                )

            self.parse_from_json(json, device_ref)

    def parse_from_json(self, json, device_ref=None):
        """Parses from the json dict

        Args:
            json (dict): json dict after json.loads()
        """
        if device_ref is None:
            raise Exception(
                "Cannot Parse Connection from JSON with no Device Reference, check device_ref parameter in constructor "
            )

        self.name = json["name"]
        self.ID = json["id"]
        self.layer = device_ref.get_layer(json["layer"])

        # Pull out the paths
        if "paths" in json["params"].keys():
            json_paths = json["params"]["paths"]
            for json_path in json_paths:
                self._paths.append(ConnectionPath(json_path))

        self.params = Params(json["params"])

        self.source = Target(json["source"])

        for target in json["sinks"]:
            self.sinks.append(Target(target))

        # TODO - Change this in the v1.2 version
        if "waypoints" in json.keys():
            waypoints_raw = json["waypoints"]
            waypoints = [(wp[0], wp[1]) for wp in waypoints_raw]
            self.add_waypoints_path(None, None, waypoints)

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    @property
    def paths(self) -> List[ConnectionPath]:
        return self._paths

    def add_waypoints_path(
        self, source: Target, sink: Target, waypoints: List[Tuple[int, int]]
    ) -> None:
        """Adds a waypoints path to the connection

        Args:
            source (Target): source target of the connection corresponding to the path
            sink (Target): sink target of the connection corresponding to the path
            waypoints (List[Tuple[int, int]]): array of coordinates (as tuples)
        """
        path = ConnectionPath(source, sink, waypoints)
        self._paths.append(path)

    def to_parchmint_v1(self):
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        ret = {
            "sinks": [s.to_parchmint_v1() for s in self.sinks],
            "name": self.name,
            "id": self.ID,
            "source": self.source.to_parchmint_v1(),
            "params": self.params.to_parchmint_v1(),
            "layer": self.layer.ID,
        }

        ret["paths"] = [path.to_parchmint_v1() for path in self._paths]

        return ret
