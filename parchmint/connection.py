from __future__ import annotations
from os import error

from typing import List, Optional, Tuple

from parchmint.layer import Layer
from parchmint.params import Params
from parchmint.target import Target


class ConnectionPath:
    """Describes the connection path which is a member of the connection, it consists of
    the source and sink targets and a list of waypoints that connect them.
    """

    def __init__(
        self,
        source: Target = None,
        sink: Target = None,
        waypoints: List[Tuple[int, int]] = None,
        json_data=None,
    ) -> None:
        """Creates a new connection path object

        Args:
            source (Target): source corresponding to the path
            sink (Target): sink corresponding to the path
            waypoints (List[Tuple[int, int]], optional): list of the coordinates. Defaults to [].
        """
        if waypoints is None:
            waypoints = []
        super().__init__()
        self.__source: Optional[Target] = source
        self.__sink: Optional[Target] = sink
        self.__waypoints: List[Tuple[int, int]] = waypoints

        if json_data is not None:
            self.parse_parchmint_v1(json_data)

    @property
    def source(self) -> Target:
        """Returns the source information of the connection path

        Raises:
            Error: No source was set in the connection path

        Returns:
            Target: Source information
        """
        if self.__source is None:
            raise error("No value set to the source")
        return self.__source

    @property
    def sink(self) -> Target:
        """Returns the sink information of the connection path

        Raises:
            Error: No sink was set in the connection path

        Returns:
            Target: Sink information
        """
        if self.__sink is None:
            raise error("No value set to the sink")
        return self.__sink

    @property
    def waypoints(self) -> List[Tuple[int, int]]:
        """Returns the waypoints in the connection path

        Returns:
            List[Tuple[int, int]]: The list of waypoints
        """
        return self.__waypoints

    @waypoints.setter
    def waypoints(self, value: List[Tuple[int, int]]):
        """Sets teh waypoints of the connection path

        Args:
            value (List[Tuple[int, int]]): List of co-ordinate tuples
        """
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

    def parse_parchmint_v1(self, json_data) -> None:
        self.__source = Target(json=json_data["source"])
        self.__sink = Target(json=json_data["sink"])
        self.__waypoints = (
            [(wp[0], wp[1]) for wp in json_data["wayPoints"]]
            if json_data["wayPoints"] is not None
            else []
        )


class Connection:
    """Connection Object represented in parchmint

    Connection object encapsulates all types of channels that can be drawn
    to connect different microfluidic components.

    """

    def __init__(self, json_data=None, device_ref=None):
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
        self.layer: Optional[Layer] = None
        self._paths: List[ConnectionPath] = []
        self.features: List[str] = []

        if json_data:
            if device_ref is None:
                raise Exception(
                    "Cannot Parse Connection from JSON with no Device Reference, check device_ref parameter in constructor "
                )

            self.parse_from_json_v1_x(json_data, device_ref)

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
        if "sinks" in json.keys():
            for target in json["sinks"]:
                self.sinks.append(Target(target))

    def parse_from_json_v1_x(self, json_data, device_ref=None):
        """Parses from the json dict - v1_x

        Args:
            json (dict): json dict after json.loads()
        """
        if device_ref is None:
            raise Exception(
                "Cannot Parse Connection from JSON with no Device Reference, check device_ref parameter in constructor "
            )
        self.name = json_data["name"]
        self.ID = json_data["id"]
        self.layer = device_ref.get_layer(json_data["layer"])

        # Pull out the paths
        if "paths" in json_data.keys():
            json_paths = json_data["paths"]
            for json_path in json_paths:
                self._paths.append(ConnectionPath(json_data=json_path))
        else:
            print("No path data found for connection {}".format(self.ID))

        self.params = Params(json_data["params"])

        self.source = Target(json_data["source"])

        if "sinks" in json_data.keys():
            if json_data["sinks"]:
                for target in json_data["sinks"]:
                    self.sinks.append(Target(target))
            else:
                print("connection", self.name, "does not have any sinks")
        else:
            print("connection", self.name, "does not have any sinks")

        if "features" in json_data.keys():
            self.features = json_data["features"]

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
            "source": self.source.to_parchmint_v1() if self.source else None,
            "params": self.params.to_parchmint_v1() if self.params else None,
            "layer": self.layer.ID if self.layer else None,
        }

        ret["paths"] = [path.to_parchmint_v1() for path in self._paths]

        return ret

    def to_parchmint_v1_x(self):
        """Returns the updated json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """

        ret = {
            "sinks": [s.to_parchmint_v1() for s in self.sinks],
            "name": self.name,
            "id": self.ID,
            "source": self.source.to_parchmint_v1() if self.source else None,
            "params": self.params.to_parchmint_v1(),
            "layer": self.layer.ID if self.layer else None,
            "paths": [path.to_parchmint_v1() for path in self._paths],
            "features": self.features,
        }

        return ret

    def __hash__(self) -> int:
        return hash(repr(self))
