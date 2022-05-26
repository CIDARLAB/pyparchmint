from __future__ import annotations

from os import error
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple

from parchmint.feature import Feature
from parchmint.layer import Layer
from parchmint.params import Params
from parchmint.target import Target

if TYPE_CHECKING:
    from parchmint.device import Device


class ConnectionPath:
    """Describes the connection path which is a member of the connection, it consists of
    the source and sink targets and a list of waypoints that connect them.
    """

    def __init__(
        self,
        source: Target,
        sink: Target,
        waypoints: Optional[List[Tuple[int, int]]] = None,
        features: Optional[List[Feature]] = None,
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
        self.__waypoints: List[Tuple[int, int]] = (
            waypoints if waypoints is not None else []
        )
        self.__features: List[Feature] = features if features is not None else []

    @property
    def features(self) -> List[Feature]:
        """Returns the features of the connection path

        Returns:
            List[str]: list of features
        """
        return self.__features

    @features.setter
    def features(self, features: List[Feature]) -> None:
        """Sets the feature array
        Args:
            features (List[str]): List of feature ids
        """
        self.__features = features

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

    @source.setter
    def source(self, source: Target) -> None:
        """Sets the source of the connection path
        Args:
            source (Target): source of the connection path
        """
        self.__source = source

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

    @sink.setter
    def sink(self, sink: Target) -> None:
        """Sets the sink of the connection path
        Args:
            sink (Target): sink of the connection path
        """
        self.__sink = sink

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

    def add_waypoint(self, x: int, y: int) -> None:
        """Adds a waypoint to the connection path

        Args:
            x (int): x co-ordinate of the waypoint
            y (int): y co-ordinate of the waypoint
        """
        self.__waypoints.append((x, y))

    def to_parchmint_v1_2(self):
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
            "features": [feat.ID for feat in self.__features],
        }

    @staticmethod
    def from_parchmint_v1_2(json_data: Dict, device_ref: Device) -> ConnectionPath:
        """Generates the connection path from the json dict for parchmint v1.2

        Args:
            json_data (Dict): JSON data dictionary
            device_ref (Device): Reference for parchmint device

        Returns:
            ConnectionPath: Connection path object
        """
        features = []
        if "features" in json_data:
            features = [
                device_ref.get_feature(feat_id) for feat_id in json_data["features"]
            ]

        ret = ConnectionPath(
            source=Target(json_data=json_data["source"]),
            sink=Target(json_data=json_data["sink"]),
            waypoints=[(wp[0], wp[1]) for wp in json_data["wayPoints"]],
            features=features,
        )

        return ret


class Connection:
    """Connection Object represented in parchmint

    Connection object encapsulates all types of channels that can be drawn
    to connect different microfluidic components.

    """

    def __init__(
        self,
        name: str = "",
        ID: str = "",
        entity: str = "",
        source: Optional[Target] = None,
        sinks: Optional[List[Target]] = None,
        params: Params = Params(),
        layer: Optional[Layer] = None,
        paths: Optional[List[ConnectionPath]] = None,
    ):
        """[summary]

        Args:
            json ([type], optional): [description]. Defaults to None.
            device_ref ([type], optional): [description]. Defaults to None.

        Raises:
            Exception: [description]
        """
        self.name: Optional[str] = name
        self.ID: str = ID
        self.entity: Optional[str] = entity
        self.params: Params = params
        self.source: Optional[Target] = source
        self.sinks: List[Target] = sinks if sinks is not None else []
        self.layer: Optional[Layer] = layer if layer is not None else None
        self._paths: List[ConnectionPath] = paths if paths is not None else []

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    @property
    def paths(self) -> List[ConnectionPath]:
        """Returns the path in the connection

        Returns:
            List[ConnectionPath]: List of paths in the connection
        """
        return self._paths

    @paths.setter
    def paths(self, value: List[ConnectionPath]):
        """Sets the connection paths

        Args:
            value (List[ConnectionPath]): a list of connection paths.
        """
        self._paths = value

    def add_path(self, path: ConnectionPath) -> None:
        """Adds a path to the connection"""

        targets = [self.source, *self.sinks]
        # Check if source and sink are in the connection
        if path.source not in targets:
            raise Exception("Source of path is not in connection")

        if path.sink not in targets:
            raise Exception("Sink of path is not in connection")

        self._paths.append(path)

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
            "source": self.source.to_parchmint_v1()
            if self.source is not None
            else None,
            "params": self.params.to_parchmint_v1(),
            "layer": self.layer.ID if self.layer is not None else None,
        }

        ret["paths"] = [path.to_parchmint_v1_2() for path in self._paths]

        return ret

    def to_parchmint_v1_2(self):
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
            "paths": [path.to_parchmint_v1_2() for path in self._paths],
            "entity": self.entity,
        }

        return ret

    def __hash__(self) -> int:
        return hash(repr(self))

    @staticmethod
    def from_parchmint_v1(json_data: Dict, device_ref: Device) -> Connection:
        """Parses from the json dict

        Args:
            json (dict): json dict after json.loads()
        """
        if device_ref is None:
            raise Exception(
                "Cannot Parse Connection from JSON with no Device Reference, check device_ref parameter in constructor "
            )

        connection = Connection()
        connection.name = json_data["name"]
        connection.ID = json_data["id"]
        connection.layer = device_ref.get_layer(json_data["layer"])

        connection.params = Params(json_data=json_data["params"])

        connection.source = Target(json_data=json_data["source"])

        if "sinks" in json_data.keys():
            if json_data["sinks"]:
                for target in json_data["sinks"]:
                    connection.sinks.append(Target(json_data=target))
            else:
                print("connection", connection.name, "does not have any sinks")
        else:
            print("connection", connection.name, "does not have any sinks")

        # TODO - Change this in the v1.2 version
        if "waypoints" in json_data.keys():
            waypoints_raw = json_data["waypoints"]
            waypoints = [(wp[0], wp[1]) for wp in waypoints_raw]
            connection.add_waypoints_path(None, None, waypoints)

        return connection

    @staticmethod
    def from_parchmint_v1_2(json_data: Dict, device_ref: Device) -> Connection:
        """Parses from the json dict

        Args:
            json (dict): json dict after json.loads()
        """
        if device_ref is None:
            raise Exception(
                "Cannot Parse Connection from JSON with no Device Reference, check device_ref parameter in constructor "
            )

        connection = Connection(
            name=json_data["name"],
            ID=json_data["id"],
            layer=device_ref.get_layer(json_data["layer"]),
            entity=json_data["entity"],
            params=Params(json_data["params"]),
            source=Target(json_data=json_data["source"]),
            sinks=[Target(json_data=sink) for sink in json_data["sinks"]]
            if "sinks" in json_data.keys()
            else [],
            paths=[
                ConnectionPath.from_parchmint_v1_2(path, device_ref)
                for path in json_data["paths"]
            ],
        )

        return connection
