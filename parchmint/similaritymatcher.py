from __future__ import annotations

from typing import TYPE_CHECKING

from networkx.algorithms.isomorphism import DiGraphMatcher

if TYPE_CHECKING:
    from parchmint import Device


class SimilarityMatcher(DiGraphMatcher):
    """Implementation of VF2 algorithm for matching undirected graphs.
    Suitable for Graph and MultiGraph instances.
    """

    def __init__(
        self,
        device1: Device,
        device2: Device,
        # semantic_information: Dict[str, NodeFilter],
        compare_params=False,
        check_connection_target=False,
    ):
        # self._semantic_information = semantic_information
        self._graph1_device = device1
        self._graph2_device = device2
        self._param_flag = compare_params
        self._connection_flag = check_connection_target
        self._graph1_in_edges = device1.graph.in_edges
        self._graph1_out_edges = device1.graph.out_edges
        self._graph2_in_edges = device2.graph.in_edges
        self._graph2_out_edges = device2.graph.out_edges
        self._graph1_in_edges_diff_list = []
        self._graph1_out_edges_diff_list = []
        self._graph2_in_edges_diff_list = []
        self._graph2_out_edges_diff_list = []
        self._graph1_param_diff_list = []
        self._graph2_param_diff_list = []
        self._graph1_layer_diff_list = []
        self._graph2_layer_diff_list = []
        self._graph1_port_diff_list = []
        self._graph2_port_diff_list = []

        super().__init__(device1.graph, device2.graph)

    def semantic_feasibility(self, G1_node: str, G2_node: str) -> bool:
        """Overriding semantic_feasibility to compare the layers, params, ports, and connections

        Args:
            G1_node (str): node 1
            G2_node (str): node 2

        Returns:
            bool: if they are semantically feasible, return true. else return false.
        """
        feasible = True

        graph1_component = self._graph1_device.get_component(G1_node)
        graph2_component = self._graph2_device.get_component(G2_node)

        # compare connectivities
        for item in self._graph1_in_edges:
            conn_g1 = self._graph1_in_edges[item]
            conn_g2 = self._graph2_in_edges[item]

            g1_source = conn_g1["source_port"]
            g2_source = conn_g2["source_port"]

            g1_sink = conn_g1["sink_port"]
            g2_sink = conn_g2["sink_port"]

            if (g1_source.component != g2_source.component) or (
                g1_source.port != g2_source.port
            ):
                print("source port wrong")
                self._graph1_in_edges_diff_list.append(g1_source.component)
                self._graph1_in_edges_diff_list.append(g1_source.port)
                self._graph2_in_edges_diff_list.append(g2_source.component)
                self._graph2_in_edges_diff_list.append(g2_source.port)
                if self._connection_flag:
                    feasible = False

            if (g1_sink.component != g2_sink.component) or (
                g1_sink.port != g2_sink.port
            ):
                print("sink port wrong")
                self._graph1_out_edges_diff_list.append(g1_sink.component)
                self._graph1_out_edges_diff_list.append(g1_sink.port)
                self._graph2_out_edges_diff_list.append(g2_sink.component)
                self._graph2_out_edges_diff_list.append(g2_sink.port)
                if self._connection_flag:
                    feasible = False

        # compare layers
        if graph1_component.layers != graph2_component.layers:
            print("layer wrong")
            self._graph1_layer_diff_list.append(graph1_component.layers)
            self._graph2_layer_diff_list.append(graph2_component.layers)
            feasible = False

        # compare params
        if graph1_component.params != graph2_component.params:
            print("params wrong")
            self._graph1_param_diff_list.append(graph1_component.params)
            self._graph2_param_diff_list.append(graph2_component.params)

            if self._param_flag is True:
                feasible = False
            else:
                feasible = True

        # compare ports
        if graph1_component.ports != graph2_component.ports:
            print("ports wrong")
            self._graph1_port_diff_list.append(graph1_component.ports)
            self._graph2_port_diff_list.append(graph2_component.ports)
            feasible = False

        return feasible

    def print_params_diff(self) -> None:
        """
        This method prints out the difference in the parameters between G1 and G2
        """
        print("----Param differences----")

        for i in range(len(self._graph1_param_diff_list)):
            print(
                f"G1: {self._graph1_param_diff_list[i]}, G2: {self._graph2_param_diff_list[i]}"
            )

        print("----End----")

    def print_layers_diff(self) -> None:
        """
        This method prints out the difference in the layers between G1 and G2
        """
        print("----Layer differences----")

        for i in range(len(self._graph1_layer_diff_list)):
            print(
                f"G1: {self._graph1_layer_diff_list[i]}, G2: {self._graph2_layer_diff_list[i]}"
            )

        print("----End----")

    def print_port_diff(self) -> None:
        """
        This method prints out the difference in the ports between G1 and G2
        """
        print("----Port differences----")

        for i in range(len(self._graph1_port_diff_list)):
            print(
                f"G1: {self._graph1_port_diff_list[i]}, G2: {self._graph2_port_diff_list[i]}"
            )

        print("----End----")

    def print_in_edges_diff(self) -> None:
        """
        This method prints out the difference in the in edges between G1 and G2
        """
        print("----In edges differences----")

        for i in range(0, len(self._graph1_in_edges_diff_list), 2):
            print(
                f"G1: {self._graph1_in_edges_diff_list[i]} -port: {self._graph1_in_edges_diff_list[i+1]}"
            )

            print(
                f"G2: {self._graph2_in_edges_diff_list[i]} -port: {self._graph2_in_edges_diff_list[i+1]}"
            )

        print("----End----")

    def print_out_edges_diff(self) -> None:
        """
        This method prints out the difference in the out edges between G1 and G2
        """
        print("----Out edges differences----")

        for i in range(0, len(self._graph1_out_edges_diff_list), 2):
            print(
                f"G1: {self._graph1_out_edges_diff_list[i]} -port: {self._graph1_out_edges_diff_list[i+1]}"
            )

            print(
                f"G2: {self._graph2_out_edges_diff_list[i]} -port: {self._graph2_out_edges_diff_list[i+1]}",
            )

        print("----End----")
