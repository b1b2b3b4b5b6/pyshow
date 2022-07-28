import csv
from tokenize import group
import xml.etree.ElementTree as ET
import jsonpickle
from node import Node
import matplotlib.pyplot as plt
import networkx as nx
import logging


class graph:
    def __init__(self, node_dict: dict) -> None:
        self.G = nx.DiGraph()
        self.node_dict = node_dict
        for p in node_dict.values():
            p: Node = p

            for n in p.nextNodeList:
                self.G.add_edge(p.name, n)

        if(nx.number_strongly_connected_components(self.G) != 1):
            logging.error(f'not strong connect')

    def show(self):
        weights = nx.get_edge_attributes(self.G, "weight")
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, edge_color='b',
                node_color='g', node_size=100)
        nx.draw_networkx_edge_labels(self.G, pos=pos, edge_labels=weights)

        plt.show()

    def get_group(self):

        def dp(node: Node, last_node: Node) -> list:
            if len(node.nextNodeList) <= 2:
                if last_node is None:
                    next_node = self.node_dict[node.nextNodeList[0]]
                else:
                    nl = list(node.nextNodeList)
                    nl.remove(last_node.name)
                    next_node = self.node_dict[nl[0]]

                ret = dp(next_node, node)
                ret.append(node.name)
                return ret
            else:
                return []

        group_dict = {}
        for node in self.node_dict.values():
            node: Node = node
            if len(node.nextNodeList) == 1:
                ret = dp(node, None)
                group_dict[ret[0]] = ret
        return group_dict
