from __future__ import annotations

import json
import pathlib
from enum import Enum
from typing import Dict, List, Optional

import jsonschema
import networkx as nx

import parchmint
from parchmint.component import Component
from parchmint.connection import Connection
from parchmint.layer import Layer
from parchmint.params import Params
from parchmint.similaritymatcher import SimilarityMatcher

PROJECT_DIR = pathlib.Path(parchmint.__file__).parent.parent.absolute()

# GM = nx.algorithms.isomorphism.GraphMatcher(device1, device2)


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

    def __eq__(self, o: object) -> bool:
        if o.__class__ is ValveType:
            return super().__eq__(o)
        elif o.__class__ is str:
            if self is ValveType.NORMALLY_OPEN and o == "NORMALLY_OPEN":
                return True
            elif self is ValveType.NORMALLY_CLOSED and o == "NORMALLY_CLOSED":
                return True
            else:
                return False
        else:
            return False


class Device:
    """The device object is the top level object for describing a microfluidic device.
    It contains the entire list of components, connections and all the relationships
    between them"""

    def __init__(self, json_data=None):
        """Creates a new device object

        Args:
            json (dict, optional): json dict after json.loads(). Defaults to None.
        """
        self.name: str = ""
        self.components: List[Component] = []
        self.connections: List[Connection] = []
        self.layers: List[Layer] = []
        self.params: Params = Params()
        self.features = []  # Store Raw JSON Objects for now
        self.xspan: Optional[int] = None
        self.yspan: Optional[int] = None
        self.G = nx.MultiDiGraph()

        # Stores the valve / connection mappings
        self._valve_map: Dict[Component, Connection] = {}
        self._valve_type_map: Dict[Component, ValveType] = {}

        if json_data:
            self.parse_from_json(json_data)
            self.generate_network()

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
        type_info: Optional[ValveType] = None,
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
        if valve in list(self._valve_map.keys()):
            self._valve_type_map[valve] = type_info
        else:
            raise KeyError(
                "Could not update type for valve: {} since it is not found in the valveMap of they device".format(
                    valve.ID
                )
            )

    # add compare function
    # -pass device, compare devices
    # - check connections, components, print if its same or not
    # - have a flag to print parameter differences

    def compare(self, device: Device) -> bool:
        """compare against the input device. Return true if they are semnatcally feasible.

        Args:
            device (Device): expected device

        Returns:
            bool: If semntically feasible, return true. Else false.
        """
        self.generate_network()

        SM = SimilarityMatcher(self, device)

        is_same = SM.is_isomorphic()
        SM.print_params_diff()
        SM.print_layers_diff()
        SM.print_port_diff()
        SM.print_in_edges_diff()
        SM.print_out_edges_diff()

        if is_same:
            print("Match!")
        else:
            print("Not Match!")

        return is_same

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
        else:
            raise Exception(
                "Could not add component since its not an instance of parchmint:Component"
            )

    def add_connection(self, connection: Connection) -> None:
        """Adds a connection object to the device

        Args:
            connection (Connection): connectin to add

        Raises:
            Exception: if the arg is not a Connection type object
        """
        if isinstance(connection, Connection):
            self.connections.append(connection)
        else:
            raise Exception(
                "Could not add component since its not an instance of parchmint:Connection"
            )

    def add_layer(self, layer: Layer) -> None:
        """Adds a layer to the device

        Args:
            layer (Layer): layer to be added to the device
        """
        if isinstance(layer, Layer):
            self.layers.append(layer)

    def get_layer(self, id: str) -> Layer:
        """Returns the layer with the corresponding id

        Args:
            id (str): id of the layer

        Raises:
            Exception: if a layer with the corresponding id is not present

        Returns:
            Layer: layer with the corresponding id
        """
        for layer in self.layers:
            if layer.ID == id:
                return layer
        raise Exception("Could not find the layer {}".format(id))

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
                assert layer.ID is not None
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

    def parse_from_json(self, json_data) -> None:
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        self.name = json_data["name"]

        # First always add the layers
        if "layers" in json_data.keys():
            for layer in json_data["layers"]:
                self.add_layer(Layer(layer))
        else:
            print("no layers found")

        # Loop through the components
        if "components" in json_data.keys():
            for component in json_data["components"]:
                self.add_component(Component(component, self))
        else:
            print("no components found")

        if "connections" in json_data.keys():
            for connection in json_data["connections"]:
                self.add_connection(Connection(connection, self))
        else:
            print("no connections found")

        if "params" in json_data.keys():
            self.params = Params(json_data["params"])

            if self.params.exists("xspan"):
                self.xspan = self.params.get_param("xspan")
            elif self.params.exists("width"):
                self.xspan = self.params.get_param("width")
            elif self.params.exists("x-span"):
                self.xspan = self.params.get_param("x-span")

            if self.params.exists("yspan"):
                self.yspan = self.params.get_param("yspan")
            elif self.params.exists("length"):
                self.yspan = self.params.get_param("length")
            elif self.params.exists("y-span"):
                self.yspan = self.params.get_param("y-span")
        else:
            print("no params found")

        if "valveMap" in json_data.keys():
            valve_map = json_data["valveMap"]

            for key, value in valve_map.items():
                self._valve_map[self.get_component(key)] = self.get_connection(value)

        if "valveTypeMap" in json_data.keys():
            valve_type_map = json_data["valveTypeMap"]

            for key, value in valve_type_map.items():
                if value is ValveType.NORMALLY_OPEN:
                    self._valve_type_map[
                        self.get_component(key)
                    ] = ValveType.NORMALLY_OPEN
                else:
                    self._valve_type_map[
                        self.get_component(key)
                    ] = ValveType.NORMALLY_CLOSED

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

    def generate_network(self) -> None:
        """Generates the underlying graph"""
        for component in self.components:
            self.G.add_node(component.ID, component_ref=component)

        for connection in self.connections:
            if connection.source is None:
                raise Exception("Source is None for connection {}".format(connection))
            sourceref = connection.source.component
            for sink in connection.sinks:
                sinkref = sink.component
                self.G.add_edge(
                    sourceref,
                    sinkref,
                    source_port=connection.source,
                    sink_port=sink,
                    connection_ref=connection,
                )

    def get_name_from_id(self, id: str) -> str:
        """Returns the name of the component with the corresponding id

        Args:
            id (str): id of the object

        Returns:
            Optional[str]: name of the corresponding object
        """
        for component in self.components:
            if component.ID == id:
                return component.name

        raise Exception("Could not find component with ID: {}".format(id))

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

    def get_component(self, id: str) -> Component:
        """Returns the component with the corresponding ID

        Args:
            id (str): id of the component

        Raises:
            Exception: if the component is not found

        Returns:
            Component: component with the corresponding id
        """
        for component in self.components:
            if component.ID == id:
                return component
        raise Exception("Could not find component with id {}".format(id))

    def get_connection(self, id: str) -> Connection:
        """Returns the connection with the corresponding id

        Args:
            id (str): id of the connection

        Raises:
            Exception: if the connection is not found

        Returns:
            Connection: connection with the corresponding id
        """
        for connection in self.connections:
            if connection.ID == id:
                return connection
        raise Exception("Could not find connection with id {}".format(id))

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

    def to_parchmint_v1_x(self) -> Dict:
        ret = self.to_parchmint_v1()

        # Modify the version of the parchmint
        ret["version"] = 1.2

        # Add the valvemap information
        valve_map = {}
        valve_type_map = {}
        for valve, connection in self._valve_map.items():
            valve_map[valve.ID] = connection.ID
        ret["valveMap"] = valve_map
        for valve, valve_type in self._valve_type_map.items():
            valve_type_map[valve.ID] = str(valve_type)
        ret["valveTypeMap"] = valve_type_map
        return ret

    @staticmethod
    def validate_V1(json_str: str) -> None:
        """Validates the json string against the schema

        Args:
            json_str (str): json string
        """
        schema_path = PROJECT_DIR.joinpath("schemas").joinpath("V1.json")
        with open(schema_path) as json_file:
            schema = json.load(json_file)
            json_data = json.loads(json_str)
            validator = jsonschema.Draft7Validator(schema)

            errors = validator.iter_errors(json_data)  # get all validation errors

            for error in errors:
                print(error)
                print("------")
