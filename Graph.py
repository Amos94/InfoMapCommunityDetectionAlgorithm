import networkx as nx

class Graph():

    graph = nx.DiGraph()

    def __init__(self):
        self.graph = nx.DiGraph()

    def createGraph(self, filename):
        file = open(filename, 'r')

        for line in file.readlines():
            nodes = line.split()
            edge = (int(nodes[0]), int(nodes[1]))
            self.graph.add_edge(*edge)

        return self.graph