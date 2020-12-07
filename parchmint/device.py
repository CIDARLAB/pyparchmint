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
        if isinstance(connection, Connection):
            self.connections.append(connection)
        else:
            raise Exception(
                "Could not add component since its not an instance of parchmint:Connection"
            )

    def add_layer(self, layer) -> None:
        if isinstance(layer, Layer):
            self.layers.append(layer)

    def get_layer(self, id: str) -> Layer:
        for layer in self.layers:
            if layer.ID == id:
                return layer
        raise Exception("Could not find the layer {}".format(id))

    def merge_netlist(self, netlist) -> None:
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

    def parse_from_json(self, json):
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

    def get_components(self):
        return self.components

    def get_connections(self):
        return self.connections

    def generate_network(self):
        for component in self.components:
            self.G.add_node(component.ID)

        for connection in self.connections:
            sourceref = connection.source.component
            for sink in connection.sinks:
                sinkref = sink.component
                self.G.add_edge(
                    sourceref,
                    sinkref,
                    source_port=connection.source,
                    sink_port=sink,
                )

    def get_name_from_id(self, id):
        for component in self.components:
            if component.ID == id:
                return component.name

    def does_component_exist(self, component):
        return component in self.components

    def component_exists(self, component_id: str) -> bool:
        for component in self.components:
            if component_id == component.ID:
                return True

        return False

    def connection_exists(self, connection_id: str) -> bool:
        for connection in self.connections:
            if connection_id == connection.ID:
                return True

        return False

    def get_component(self, id: str) -> Component:
        for component in self.components:
            if component.ID == id:
                return component
        raise Exception("Could not find component with id {}".format(id))

    def get_connection(self, id: str) -> Connection:
        for connection in self.connections:
            if connection.ID == id:
                return connection
        raise Exception("Could not find connection with id {}".format(id))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
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
        schema_path = PROJECT_DIR.joinpath("schemas").joinpath("V1.json")
        with open(schema_path) as json_file:
            schema = json.load(json_file)
            json_data = json.loads(json_str)
            validator = jsonschema.Draft7Validator(schema)

            errors = validator.iter_errors(json_data)  # get all validation errors

            for error in errors:
                print(error)
                print("------")
