from __future__ import annotations
from os import truncate
# from parchmint.device import Device
from typing import Dict
from networkx.algorithms.isomorphism import DiGraphMatcher
from networkx.classes import digraph
# from reggie.nodefilter import NodeFilter
# from lfr.fig.fluidinteractiongraph import FluidInteractionGraph


class SimilarityMatcher(DiGraphMatcher):
    """Implementation of VF2 algorithm for matching undirected graphs.
    Suitable for Graph and MultiGraph instances.
    """

    def __init__(
        self,
        G1,
        G2,
        # semantic_information: Dict[str, NodeFilter],
        compare_params=False
    ):
        # self._semantic_information = semantic_information
        self.G1_device = G1
        self.G2_device = G2
        self.compare_params = compare_params
        self.G1_param_diff_list = []
        self.G2_param_diff_list = []
        self.G1_layer_diff_list = []
        self.G2_layer_diff_list = []
        self.G1_port_diff_list = []
        self.G2_port_diff_list = []

        super(SimilarityMatcher, self).__init__(G1.G, G2.G)

    def semantic_feasibility(self, G1_node, G2_node) -> bool:
        """Returns True if adding (G1_node, G2_node) is symantically feasible.
        The semantic feasibility function should return True if it is
        acceptable to add the candidate pair (G1_node, G2_node) to the current
        partial isomorphism mapping.   The logic should focus on semantic
        information contained in the edge data or a formalized node class.
        By acceptable, we mean that the subsequent mapping can still become a
        complete isomorphism mapping.  Thus, if adding the candidate pair
        definitely makes it so that the subsequent mapping cannot become a
        complete isomorphism mapping, then this function must return False.
        The default semantic feasibility function always returns True. The
        effect is that semantics are not considered in the matching of G1
        and G2.
        The semantic checks might differ based on the what type of test is
        being performed.  A keyword description of the test is stored in
        self.test.  Here is a quick description of the currently implemented
        tests::
          test='graph'
            Indicates that the graph matcher is looking for a graph-graph
            isomorphism.
          test='subgraph'
            Indicates that the graph matcher is looking for a subgraph-graph
            isomorphism such that a subgraph of G1 is isomorphic to G2.
        Any subclass which redefines semantic_feasibility() must maintain
        the above form to keep the match() method functional. Implementations
        should consider multigraphs.
        """

        # check each components. If not same, print out the difference and return false. 
        feasible = True


        G1_component = self.G1_device.get_component(G1_node)
        G2_component = self.G2_device.get_component(G2_node)


        if G1_component.layers != G2_component.layers:
          print("layer wrong")
          feasible = False
        
        # store all the differences

        if G1_component.params != G2_component.params:
          print("params wrong")
          self.G1_param_diff_list.append(G1_component.params)
          self.G2_param_diff_list.append(G2_component.params)

          if self.compare_params is True:
            feasible = False
          else:
            feasible = True          

        if G1_component.ports != G2_component.ports:
          print("ports wrong")
          feasible = False

        return feasible        
      
      
    def print_params_diff(self) -> None:
      """
      This method prints out the difference in the parameters between G1 and G2
      """

      print("----Param differences----")

      for i in range(len(self.G1_param_diff_list)):
        print(f'G1: {self.G1_param_diff_list[i]}, G2: {self.G2_param_diff_list[i]}')

      print("----End----")

    
    def print_layers_diff(self) -> None:
      """
      This method prints out the difference in the layers between G1 and G2
      """

      print("----Layer differences----")

      for i in range(len(self.G1_layer_diff_list)):
        print(f'G1: {self.G1_layer_diff_list[i]}, G2: {self.G2_layer_diff_list[i]}')

      print("----End----")


    def print_port_diff(self) -> None:
      """
      This method prints out the difference in the ports between G1 and G2
      """

      print("----Layer differences----")

      for i in range(len(self.G1_port_diff_list)):
        print(f'G1: {self.G1_port_diff_list[i]}, G2: {self.G2_port_diff_list[i]}')

      print("----End----")