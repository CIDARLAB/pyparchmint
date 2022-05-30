from __future__ import annotations

import json
import pathlib
from enum import Enum
from typing import Dict, List, Optional
from warnings import warn

import jsonschema
import networkx as nx

from parchmint.component import Component
from parchmint.connection import Connection
from parchmint.feature import Feature
from parchmint.layer import Layer
from parchmint.params import Params
from parchmint.similaritymatcher import SimilarityMatcher

PROJECT_DIR = pathlib.Path(__file__).parent.parent.absolute()


class ValveType(Enum):
    """Types of the valves"""

    NORMALLY_OPEN = 0
    NORMALLY_CLOSED = 1

    def __str__(self) -> str:
        if self == ValveType.NORMALLY_OPEN:
            return "NORMALLY_OPEN"
        elif self == ValveType.NORMALLY_CLOSED:
            return "NORMALLY_CLOSED"
        else:
            raise Exception("Could not generate Valve Type string")

    def __eq__(self, object_to_compare: object) -> bool:
        if object_to_compare.__class__ is ValveType:
            return super().__eq__(object_to_compare)
        elif object_to_compare.__class__ is str:
            if self is ValveType.NORMALLY_OPEN and object_to_compare == "NORMALLY_OPEN":
                return True
            elif (
                self is ValveType.NORMALLY_CLOSED
                and object_to_compare == "NORMALLY_CLOSED"
            ):
                return True
            else:
                return False
        else:
            return False


class Device:
    """The device object is the top level object for describing a microfluidic device.
    It contains the entire list of components, connections and all the relationships
    between them"""

    def __init__(self, name: str = ""):
        """Creates a new device object

        Args:
            json (dict, optional): json dict after json.loads(). Defaults to None.
        """
        self.name: str = name
        self.components: List[Component] = []
        self.connections: List[Connection] = []
        self.layers: List[Layer] = []
        self.params: Params = Params()
        self.features: List[Feature] = []  # Store Raw JSON Objects for now
        self.params.set_param("x-span", 0)
        self.params.set_param("y-span", 0)
        self.features = []  # Store Raw JSON Objects for now
        self.graph = nx.MultiDiGraph()

        # Stores the valve / connection mappings
        self._valve_map: Dict[Component, Connection] = {}
        self._valve_type_map: Dict[Component, ValveType] = {}

    @property
    def xspan(self) -> Optional[int]:
        """Returns the x span of the device
        Returns:
            int: x span of the device
        """
        return self.params.get_param("x-span") if self.params.exists("x-span") else None

    @xspan.setter
    def xspan(self, xspan: int) -> None:
        """Sets the x span of the device
        Args:
            xspan (int): x span of the device
        """
        self.params.set_param("x-span", xspan)

    @property
    def yspan(self) -> Optional[int]:
        """Returns the y span of the device
        Returns:
            int: y span of the device
        """
        return self.params.get_param("y-span") if self.params.exists("y-span") else None

    @yspan.setter
    def yspan(self, yspan: int) -> None:
        """Sets the y span of the device
        Args:
            yspan (int): y span of the device
        """
        self.params.set_param("y-span", yspan)

    def get_feature(self, feature_id: str) -> Feature:
        """Returns the feature object with the given name

        Args:
            name (str): name of the feature

        Returns:
            Feature: Feature object with the given name
        """
        for feature in self.features:
            if feature.ID == feature_id:
                return feature
        raise Exception("Feature not found")

    @property
    def valves(self) -> List[Component]:
        """Returns the valve components in the device

        Returns:
            List[Component]: List of valve components in the device
        """
        return list(self._valve_map.keys())

    def map_valve(
        self,
        valve: Component,
        connection: Connection,
        type_info: ValveType = ValveType.NORMALLY_OPEN,
    ) -> None:
        """Maps the valve to a connection in the device

        Args:
            valve (Component): valve component
            connection (Connection): connection on which the valve is mapped
            type_info (Optional[ValveType]): Type informaiton of the valve

        """
        self._valve_map[valve] = connection
        if type_info is not None:
            self.update_valve_type(valve, type_info)

    def get_valves(self) -> List[Component]:
        """Returns the list of valves in the device

        Returns:
            List[Component]: Valve Component Objects
        """
        return list(self._valve_map.keys())

    def get_valve_connection(self, valve: Component) -> Connection:
        """Returns the connection associated with the valve object

        Args:
            valve (Component): Valve object for which we are finding the connection

        Returns:
            Connection: connection object on which the valve is placed
        """
        return self._valve_map[valve]

    def update_valve_type(self, valve: Component, type_info: ValveType) -> None:
        """Updates the type of the valve to normally closed  or normally open

        Args:
            valve (Component): Valve object we want to update
            type_info (ValveType): Valve Type

        Raises:
            KeyError: Raises the error if the valve object is not mapped as a valve in the device
        """
        if valve in self._valve_map:
            self._valve_type_map[valve] = type_info
        else:
            raise KeyError(
                "Could not update type for valve: {} since it is not found in the valveMap of they device".format(
                    valve.ID
                )
            )

    def remove_valve(self, valve_id) -> None:
        """Removes the valve entry from the device, also deletes the component from the device's components

        Args:
            valve_id (str): ID of the valve to be removed
        """
        for valve in self.valves:
            if valve.ID == valve_id:
                self._valve_map.pop(valve)
                self._valve_type_map.pop(valve)
                break

        self.remove_component(valve_id)

    def compare(self, device: Device, compare_params: bool = False) -> bool:
        """compare against the input device. Return true if they are semnatcally feasible.

        Args:
            device (Device): expected device
            compare_params (bool): comparision includes parameter differences. Defaults to False.

        Returns:
            bool: If semntically feasible, return true. Else false.
        """
        matcher = SimilarityMatcher(self, device, compare_params=compare_params)

        is_same = matcher.is_isomorphic()
        matcher.print_params_diff()
        matcher.print_layers_diff()
        matcher.print_port_diff()
        matcher.print_in_edges_diff()
        matcher.print_out_edges_diff()

        if is_same:
            print("Match!")
        else:
            print("Not Match!")

        return is_same

    def add_feature(self, feature: Feature) -> None:
        """Adds a feature to the device
        Args:
            feature (Feature): Feature object to be added
        """
        self.features.append(feature)

    def remove_feature(self, feature_id: str) -> None:
        """Removes a feature from the device
        Args:
            feature_id (str): ID of the feature to be removed
        Raises:
            Exception: Raises the error if the feature is not found in the device
        """
        for feature in self.features:
            if feature.ID == feature_id:
                self.features.remove(feature)
                return
        raise Exception("Feature not found")

    def add_component(self, component: Component) -> None:
        """Adds a component object to the device

        Args:
            component (Component): component to eb added

        Raises:
            Exception: if the passed object is not a Component instance
        """
        if isinstance(component, Component):
            # Check if Component Exists, if it does ignore it
            if self.component_exists(component.ID):
                print(
                    "Component {} already present in device, "
                    "hence skipping the component".format(component.name)
                )
            self.components.append(component)
            self.graph.add_node(component.ID)
        else:
            raise Exception(
                "Could not add component since its not an instance of parchmint:Component"
            )

    def remove_component(self, component_id: str) -> None:
        """Removes a component object from the device

        Args:
            component_id (str): ID of the component to be removed

        Raises:
            Exception: Raises the error if the component is not found in the device
        """
        for component in self.components:
            if component.ID == component_id:
                self.components.remove(component)
                self.graph.remove_node(component_id)
                return
        raise Exception("Component not found")

    def add_connection(self, connection: Connection) -> None:
        """Adds a connection object to the device

        Args:
            connection (Connection): connectin to add

        Raises:
            Exception: if the arg is not a Connection type object
        """
        if isinstance(connection, Connection):
            # Check if the source component is present in the device
            if connection.source is None:
                raise Exception("Connection source is not defined")

            if self.component_exists(connection.source.component) is False:
                raise Exception(
                    "Source component {} not found in the device while adding connection: {}".format(
                        connection.source, connection.ID
                    )
                )

            # Check if the connection sinks are defined / exist in the device
            if len(connection.sinks) == 0:
                print(
                    "Warning: No sinks defined for connection {}".format(
                        connection.name
                    )
                )

            for sink in connection.sinks:
                if self.component_exists(sink.component) is False:
                    raise Exception(
                        "Sink component {} not found in the device while adding connection: {}".format(
                            sink, connection.name
                        )
                    )

            self.connections.append(connection)
            # Connect the components associated here on the nx graph
            for sink in connection.sinks:
                self.graph.add_edge(
                    connection.source.component,
                    sink.component,
                    source_port=connection.source,
                    sink_port=sink,
                    connection_ref=connection,
                    connection_id=connection.ID,
                )
        else:
            raise Exception(
                "Could not add component since its not an instance of parchmint:Connection"
            )

    def remove_connection(self, connection_id: str) -> None:
        """Removes a connection object from the device

        Args:
            connection_id (str): ID of the connection to be removed

        Raises:
            Exception: Raises the error if the connection is not found in the device
        """
        for connection in self.connections:
            if connection.ID == connection_id:
                self.connections.remove(connection)
                if connection.source is not None:
                    for sink in connection.sinks:
                        self.graph.remove_edge(
                            connection.source.component, sink.component
                        )
                return
        raise Exception("Connection not found")

    def add_layer(self, layer: Layer) -> None:
        """Adds a layer to the device

        Args:
            layer (Layer): layer to be added to the device
        """
        if isinstance(layer, Layer):
            self.layers.append(layer)

    def remove_layer(self, layer_id: str) -> None:
        """Removes a layer from the device, also removes all the components and connections corresponding to the layer

        Args:
            layer_id (str): ID of the layer to be removed
        """
        layer_to_delete = None
        for layer in self.layers:
            if layer.ID == layer_id:
                layer_to_delete = layer

        if layer_to_delete is None:
            raise Exception("Layer not found")

        # Remove all the components and connections associated with the layer
        for component in self.components:
            if {[layer.ID for layer in component.layers]} == set(layer_to_delete.ID):
                self.remove_component(component.ID)
            else:
                warn(
                    "Skipped removing component {} from the device".format(component.ID)
                )

        for connection in self.connections:
            if connection.layer is None:
                continue
            if layer_to_delete.ID == connection.layer.ID:
                self.remove_connection(connection.ID)

    def get_layer(self, layer_id: str) -> Layer:
        """Returns the layer with the corresponding id

        Args:
            layer_id (str): id of the layer

        Raises:
            Exception: if a layer with the corresponding id is not present

        Returns:
            Layer: layer with the corresponding id
        """
        for layer in self.layers:
            if layer.ID == layer_id:
                return layer
        raise Exception("Could not find the layer {}".format(layer_id))

    def merge_netlist(self, netlist: Device) -> None:
        """Merges two netlists together. Currently assumes that both
        devices have the same ordering of layers

        Args:
            netlist (Device): netlist to merge
        """
        # TODO - Figure out how to merge the layers later
        # First create a map of layers
        layer_mapping = {}
        for layer in netlist.layers:
            if layer not in self.layers:
                self.add_layer(layer)
                layer_mapping[layer] = layer
            else:
                if layer.ID is None:
                    raise Exception("Layer ID is None, cannot merge the layers")
                layer_mapping[layer] = self.get_layer(layer.ID)

        for component in netlist.components:
            new_layers = []
            for layer in component.layers:
                new_layers.append(layer_mapping[layer])
            component.layers = new_layers
            self.add_component(component)

        for connection in netlist.connections:
            connection.layer = layer_mapping[connection.layer]
            self.add_connection(connection)

    def get_components(self) -> List[Component]:
        """Returns the components in the device

        Returns:
            List[Component]: list of components in the device
        """
        return self.components

    def get_connections(self) -> List[Connection]:
        """Returns the connections in the device

        Returns:
            List[Connection]: list of connections in the device
        """
        return self.connections

    def get_connection_between_components(self, source, sink) -> Connection:
        """Returns the connection between two components

        Args:
            source (Component): source component
            sink (Component): sink component

        Returns:
            Connection: connection between the two components
        """
        return self.graph.get_edge_data(source, sink)["connection_ref"]

    def get_name_from_id(self, component_id: str) -> str:
        """Returns the name of the component with the corresponding id

        Args:
            id (str): id of the object

        Returns:
            Optional[str]: name of the corresponding object
        """
        for component in self.components:
            if component.ID == component_id:
                return component.name

        raise Exception("Could not find component with ID: {}".format(component_id))

    def component_exists(self, component_id: str) -> bool:
        """checks if component exists in the device

        Args:
            component_id (str): id of the component

        Returns:
            bool: true if the component exists
        """
        for component in self.components:
            if component_id == component.ID:
                return True

        return False

    def connection_exists(self, connection_id: str) -> bool:
        """checks if connection exists in the device

        Args:
            connection_id (str): id of the connection

        Returns:
            bool: true if the connection exists
        """
        for connection in self.connections:
            if connection_id == connection.ID:
                return True

        return False

    def get_component(self, component_id: str) -> Component:
        """Returns the component with the corresponding ID

        Args:
            id (str): id of the component

        Raises:
            Exception: if the component is not found

        Returns:
            Component: component with the corresponding id
        """
        for component in self.components:
            if component.ID == component_id:
                return component
        raise Exception("Could not find component with id {}".format(component_id))

    def get_connection(self, component_id: str) -> Connection:
        """Returns the connection with the corresponding id

        Args:
            id (str): id of the connection

        Raises:
            Exception: if the connection is not found

        Returns:
            Connection: connection with the corresponding id
        """
        for connection in self.connections:
            if connection.ID == component_id:
                return connection
        raise Exception("Could not find connection with id {}".format(component_id))

    def get_connections_for_edge(
        self, source: Component, sink: Component
    ) -> List[Connection]:
        """Returns the connections for the given edge

        Args:
            source (Component): source component
            sink (Component): sink component

        Returns:
            List[Connection]: list of connections for the given edge
        """
        try:
            return [
                edge["connection_ref"]
                for edge in list((self.graph[source.ID][sink.ID]).values())
            ]
        except KeyError:
            print(
                "Warning ! - No connections found between {} and {}".format(
                    source, sink
                )
            )
            return []

    def get_connections_for_component(self, component: Component) -> List[Connection]:
        """Returns the connections for the given component

        Args:
            component (Component): component

        Returns:
            List[Connection]: list of connections for the given component
        """
        edge_list = list(self.graph.in_edges(component.ID))
        edge_list.extend(list(self.graph.out_edges(component.ID)))
        connections = [
            self.graph.get_edge_data(*e)[0]["connection_ref"] for e in edge_list
        ]
        return connections

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        ret = {}
        ret["name"] = self.name
        ret["components"] = [c.to_parchmint_v1() for c in self.components]
        ret["connections"] = [c.to_parchmint_v1() for c in self.connections]
        ret["params"] = self.params.to_parchmint_v1()
        ret["layers"] = [layer.to_parchmint_v1() for layer in self.layers]
        ret["version"] = 1

        return ret

    def to_parchmint_v1_2(self) -> Dict:
        """Generating the parchmint v1.2 of the device

        Returns:
            Dict: dictionary that can be used in json.dumps()
        """
        self.params.set_param("x-span", self.xspan)
        self.params.set_param("y-span", self.yspan)
        ret = {}
        ret["name"] = self.name
        ret["components"] = [c.to_parchmint_v1() for c in self.components]
        ret["connections"] = [c.to_parchmint_v1_2() for c in self.connections]
        ret["params"] = self.params.to_parchmint_v1()
        ret["layers"] = [layer.to_parchmint_v1() for layer in self.layers]

        ret["features"] = [feature.to_parchmint_v1_2() for feature in self.features]

        # Modify the version of the parchmint
        ret["version"] = "1.2"

        # Add the valvemap information
        valve_objects = []
        for valve, connection in self._valve_map.items():
            valve_object = {
                "componentid": valve.ID,
                "connectionid": connection.ID,
                "type": str(self._valve_type_map[valve]),
            }
            valve_objects.append(valve_object)
        ret["valves"] = valve_objects

        return ret

    @staticmethod
    def validate_v1(json_str: str) -> None:
        """Validates the json string against the schema

        Args:
            json_str (str): json string
        """
        schema_path = PROJECT_DIR.joinpath("schemas").joinpath("parchmint_v1.json")
        with open(schema_path, encoding="utf-8") as json_file:
            schema = json.load(json_file)
            json_data = json.loads(json_str)
            validator = jsonschema.Draft7Validator(schema)

            errors = validator.iter_errors(json_data)  # get all validation errors

            is_empty = True
            for error in errors:
                is_empty = False
                print(error)
                print("------")

            if is_empty:
                print("No errors found")

    @staticmethod
    def validate_v1_2(json_str: str) -> None:
        """Validates the json string against the schema

        Args:
            json_str (str): json string
        """
        schema_path = PROJECT_DIR.joinpath("schemas").joinpath("parchmint_v1_2.json")
        with open(schema_path, encoding="utf-8") as json_file:
            schema = json.load(json_file)
            json_data = json.loads(json_str)
            validator = jsonschema.Draft7Validator(schema)

            errors = validator.iter_errors(json_data)  # get all validation errors

            is_empty = True
            for error in errors:
                is_empty = False
                print(error)
                print("------")

            if is_empty:
                print("No errors found")

    @staticmethod
    def from_json(json_str: str) -> Device:
        """Creates a device from a json string

        Args:
            json_str (str): json string

        Returns:
            Device: device created from the json string
        """
        ret = Device("")
        json_data = json.loads(json_str)
        json_version = json_data["version"]

        if json_version == "1.0":
            ret = Device.from_parchmint_v1(json_data)
        elif json_version == "1.1":
            ret = Device.from_parchmint_v1_2(json_data)

        return ret

    @staticmethod
    def from_parchmint_v1(json_data: Dict) -> Device:
        """Parses the json string and creates the device for Version = 1.0

        Returns:
            dict: JSON Dictionary
        """
        device_ref = Device("")

        device_ref.name = json_data["name"]

        # First always add the layers
        if "layers" in json_data.keys():
            for layer in json_data["layers"]:
                device_ref.add_layer(Layer(json_data=layer))
        else:
            print("no layers found")

        # Loop through the components
        if "components" in json_data.keys():
            for component_json in json_data["components"]:
                component = Component.from_parchmint_v1(component_json, device_ref)
                device_ref.add_component(component)
        else:
            print("no components found")

        if "connections" in json_data.keys():
            for connection_json in json_data["connections"]:
                connection = Connection.from_parchmint_v1(connection_json, device_ref)
                device_ref.add_connection(connection)
        else:
            print("no connections found")

        if "params" in json_data.keys():
            device_ref.params = Params(json_data["params"])

            if device_ref.params.exists("xspan"):
                device_ref.xspan = device_ref.params.get_param("xspan")
            elif device_ref.params.exists("width"):
                device_ref.xspan = device_ref.params.get_param("width")
            elif device_ref.params.exists("x-span"):
                device_ref.xspan = device_ref.params.get_param("x-span")

            if device_ref.params.exists("yspan"):
                device_ref.yspan = device_ref.params.get_param("yspan")
            elif device_ref.params.exists("length"):
                device_ref.yspan = device_ref.params.get_param("length")
            elif device_ref.params.exists("y-span"):
                device_ref.yspan = device_ref.params.get_param("y-span")
        else:
            print("no params found")

        def get_valve_type(value: str):
            if value is ValveType.NORMALLY_OPEN:
                return ValveType.NORMALLY_OPEN
            elif value is ValveType.NORMALLY_CLOSED:
                return ValveType.NORMALLY_CLOSED
            else:
                raise Exception("Unknown valve type {}".format(value))

        if "valveMap" in json_data.keys():
            valve_map = json_data["valveMap"]
            valve_type_map = json_data["valveTypeMap"]

            for key, value in valve_map.items():
                device_ref.map_valve(
                    device_ref.get_component(key),
                    device_ref.get_connection(value),
                    get_valve_type(valve_type_map[key]),
                )

        return device_ref

    @staticmethod
    def from_parchmint_v1_2(json_data: Dict) -> Device:
        """Parses the json string and creates the device for Version = 1.2

        Returns:
            dict: JSON Dictionary
        """
        device_ref = Device("")
        device_ref.name = json_data["name"]

        # First always add the layers
        if "layers" in json_data.keys():
            for layer in json_data["layers"]:
                device_ref.add_layer(Layer(json_data=layer))
        else:
            print("no layers found")

        # Second add all the features
        if "features" in json_data.keys():
            for feature_json in json_data["features"]:
                feature = Feature.from_parchmint_v1_2(feature_json, device_ref)
                device_ref.add_feature(feature)

        # Loop through the components
        if "components" in json_data.keys():
            for component_json in json_data["components"]:
                component = Component.from_parchmint_v1_2(component_json, device_ref)
                device_ref.add_component(component)
        else:
            print("no components found")

        if "connections" in json_data.keys():
            for connection_json in json_data["connections"]:
                connection = Connection.from_parchmint_v1_2(connection_json, device_ref)
                device_ref.add_connection(connection)
        else:
            print("no connections found")

        if "params" in json_data.keys():
            device_ref.params = Params(json_data["params"])

            if device_ref.params.exists("x-span"):
                device_ref.xspan = device_ref.params.get_param("x-span")

            if device_ref.params.exists("y-span"):
                device_ref.yspan = device_ref.params.get_param("y-span")
        else:
            print("no params found")

        def get_valve_type(value: str) -> ValveType:
            if value == ValveType.NORMALLY_OPEN:
                return ValveType.NORMALLY_OPEN
            elif value == ValveType.NORMALLY_CLOSED:
                return ValveType.NORMALLY_CLOSED
            else:
                raise Exception("Unknown valve type {}".format(value))

        if "valves" in json_data.keys():
            valve_objects = json_data["valves"]

            for valve_object in valve_objects:
                componentid = valve_object["componentid"]
                connectionid = valve_object["connectionid"]
                # Note - Sets it to default normally open if nothign is specified
                valve_type = valve_object["type"] if "type" in valve_object else None
                device_ref.map_valve(
                    device_ref.get_component(componentid),
                    device_ref.get_connection(connectionid),
                    get_valve_type(valve_type)
                    if valve_type is not None
                    else ValveType.NORMALLY_OPEN,
                )

        return device_ref
