from parchmint.layer import Layer
import networkx as nx
from typing import Optional, List
from parchmint.component import Component
from parchmint.connection import Connection
from parchmint.params import Params
from parchmint.layer import Layer


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
        self.G = nx.MultiGraph()

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
            raise Exception("Could not add component since its not an instance of parchmint:Component")

    def add_connection(self, connection: Connection):
        if isinstance(connection, Connection):
            self.connections.append(connection)
        else:
            raise Exception("Could not add component since its not an instance of parchmint:Connection")

    def add_layer(self, layer):
        if isinstance(layer, Layer):
            self.layers.append(layer)

    def merge_netlist(self, netlist: Device):
        # TODO - Figure out how to merge the layers later
        for layer in netlist.layers:
            if layer not in self.layers:
                self.add_layer(layer)

        for component in netlist.components:
            self.add_component(component)

        for connection in netlist.connections:
            self.add_connection(connection)

    def parse_from_json(self, json):
        self.name = json["name"]

        # Loop through the components
        for component in json["components"]:
            self.add_component(Component(component))

        for connection in json["connections"]:
            self.add_connection(Connection(connection))

        if "params" in json.keys():
            self.params = Params(json["params"])

            if self.params.exists("xspan"):
                self.xspan = self.params.get_param("xspan")
            elif self.params.exists("width"):
                self.xspan = self.params.get_param("width")

            if self.params.exists("yspan"):
                self.yspan = self.params.get_param("yspan")
            elif self.params.exists("length"):
                self.yspan = self.params.get_param("length")

        for layer in json["layers"]:
            self.add_layer(Layer(layer))

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

    def get_component(self, id: str) -> Optional[Component]:
        if self.component_exists(id):
            for component in self.components:
                if component.ID == id:
                    return component
        else:
            return None

    def get_connection(self, id: str) -> Optional[Connection]:
        if self.connection_exists(id):
            for connection in self.connections:
                if connection.ID == id:
                    return connection
        else:
            return None

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

    def to_parchmint_v1(self):
        return {
            "name": self.name,
            "components": [c.to_parchmint_v1() for c in self.components],
            "connections": [c.to_parchmint_v1() for c in self.connections],
            "params": self.params.to_parchmint_v1(),
            "version": 1,
            "layers": [layer.to_parchmint_v1() for layer in self.layers],
        }

