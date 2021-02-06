from __future__ import annotations
from parchmint.layer import Layer
import networkx as nx
from typing import Optional, List
from parchmint.component import Component
from parchmint.connection import Connection
from parchmint.params import Params
import jsonschema
import pathlib
import parchmint
import json

PROJECT_DIR = pathlib.Path(parchmint.__file__).parent.parent.absolute()


class Device:
    def __init__(self, json=None):
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

        if json:
            self.parse_from_json(json)
            self.generate_network()

    def add_component(self, component: Component):
        """Adds a component object to the device

        Args:
            component (Component): component to eb added

        Raises:
            Exception: if the passed object is not a Component instance
        """
        if isinstance(component, Component):
            # Check if Component Exists, if it does ignore it
            if self.does_component_exist(component):
                print(
                    "Component {} already present in device, "
                    "hence skipping the component".format(component.name)
                )
            self.components.append(component)
        else:
            raise Exception(
                "Could not add component since its not an instance of parchmint:Component"
            )

    def add_connection(self, connection: Connection):
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
        layer_mapping = dict()
        for layer in netlist.layers:
            if layer not in self.layers:
                self.add_layer(layer)
                layer_mapping[layer] = layer
            else:
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

    def parse_from_json(self, json) -> None:
        """Returns the json dict

        Returns:
            dict: dictionary that can be used in json.dumps()
        """
        self.name = json["name"]

        # First always add the layers
        for layer in json["layers"]:
            self.add_layer(Layer(layer))

        # Loop through the components
        for component in json["components"]:
            self.add_component(Component(component, self))

        for connection in json["connections"]:
            self.add_connection(Connection(connection, self))

        if "params" in json.keys():
            self.params = Params(json["params"])

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
            sourceref = connection.source._component
            for sink in connection.sinks:
                sinkref = sink._component
                self.G.add_edge(
                    sourceref,
                    sinkref,
                    source_port=connection.source,
                    sink_port=sink,
                    connection_ref=connection,
                )

    def get_name_from_id(self, id: str) -> Optional[str]:
        """Returns the name of the component with the corresponding id

        Args:
            id (str): id of the object

        Returns:
            Optional[str]: name of the corresponding object
        """
        for component in self.components:
            if component.ID == id:
                return component.name

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
        ret = dict()
        ret["name"] = self.name
        ret["components"] = [c.to_parchmint_v1() for c in self.components]
        ret["connections"] = [c.to_parchmint_v1() for c in self.connections]
        ret["params"] = self.params.to_parchmint_v1()
        ret["layers"] = [layer.to_parchmint_v1() for layer in self.layers]
        ret["version"] = 1

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
