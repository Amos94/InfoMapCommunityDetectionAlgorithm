import matplotlib
import infomap
import networkx as nx
import networkx.algorithms as nalgos
import matplotlib.pyplot as plt
import matplotlib.colors as colors
#%matplotlib inline
import pandas as pd
#import igraph as ig
#import plotly.plotly as py
#import plotly.graph_objs as go
from Graph import Graph

class Infomap():

    graph = Graph()
    def __init__(self, G):
        self.graph = G

    def findCommunities(self, G):
        """
        Partition network with the Infomap algorithm.
        Annotates nodes with 'community' id and return number of communities found.
        """
        infomapWrapper = infomap.Infomap("--two-level --undirected")
        network = infomapWrapper.network()

        print("Building Infomap network from a NetworkX graph...")
        for e in G.edges():
            network.addLink(*e)

        print("Find communities with Infomap...")
        infomapWrapper.run()

        tree = infomapWrapper.iterTree()

        print("Found %d modules with codelength: %f" % (infomapWrapper.numTopModules(), infomapWrapper.codelength()))

        communities = {}
        for node in infomapWrapper.iterLeafNodes():
            communities[node.physicalId] = node.moduleIndex()

        nx.set_node_attributes(G, name='community', values=communities)
        return infomapWrapper.numTopModules()

    def drawNetwork(self, G):
        # position map
        pos = nx.spring_layout(G)
        # community ids
        communities = [v for k, v in nx.get_node_attributes(G, 'community').items()]
        numCommunities = max(communities) + 1
        # color map from http://colorbrewer2.org/
        cmapLight = colors.ListedColormap(['#a6cee3', '#b2df8a', '#fb9a99', '#fdbf6f', '#cab2d6'], 'indexed',
                                          numCommunities)
        cmapDark = colors.ListedColormap(['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a'], 'indexed',
                                         numCommunities)

        # Draw edges
        nx.draw_networkx_edges(G, pos)

        # Draw nodes
        nodeCollection = nx.draw_networkx_nodes(G,
                                                pos=pos,
                                                node_color=communities,
                                                cmap=cmapLight
                                                )
        # Set node border color to the darker shade
        darkColors = [cmapDark(v) for v in communities]
        nodeCollection.set_edgecolor(darkColors)

        # Draw node labels
        for n in G.nodes():
            plt.annotate(n,
                         xy=pos[n],
                         textcoords='offset points',
                         horizontalalignment='center',
                         verticalalignment='center',
                         xytext=[0, 0],
                         color=cmapDark(communities[n-1])
                         )

        plt.axis('off')
        plt.savefig("image.png")
        plt.show()

    def plot3D(self, G):
        pass

    def visualize(self, G):
        self.findCommunities(G)
        self.drawNetwork(G)

    def getNumberOfConnectedComponents(self, G):
        return nalgos.number_connected_components(G)

    def getNumberOfCliques(self, G):
        return nalgos.number_of_cliques(G)

    def getNumberOfStronglyConnectedComponents(self, G):
        return nalgos.number_strongly_connected_components(G)

    def getNumberOfWeaklyConnectedComponents(self, G):
        return nalgos.number_weakly_connected_components(G)

    def getNumberOfIsolates(self, G):
        return nalgos.number_of_isolates(G)

    def getDegreeCentrality(self, G):
        return nalgos.degree_centrality(G)

    def getBetweenessCentrality(self, G):
        return nalgos.betweenness_centrality(G)

    def getAllPairsShortestPath(self, G):
        return nalgos.all_pairs_shortest_path(G)

    def getAllPairsNodeConnectivity(self, G):
        return nalgos.all_pairs_node_connectivity(G)

    def getClosenessCentrality(self, G):
        return nalgos.closeness_centrality(G)

    def getBridges(self, G):
        return nalgos.bridges(G)

    def getConnectedComponents(self,G):
        return nalgos.connected_components(G)

    def getDiameter(self,G):
        return nalgos.diameter(G)

    def getKatzCentrality(self, G):
        return nalgos.katz_centrality

    def getPageRank(self,G):
        return nalgos.pagerank(G)

    def getTriangles(self,G):
        return nalgos.triangles(G)

    def getNeighbours(self, G, vertex):
        neighbourList = []
        for neighbour in G:
            neighbourList.append(neighbour)
        return neighbourList

obj = Graph()
graph = obj.createGraph("Data//coauthorship.txt")

print("Network info:")
print("Nodes:{}, Edges:{}, Self loops:{}".format(graph.number_of_nodes(), graph.number_of_edges(), graph.number_of_selfloops()))
print("Graph type: " + "undirected" if graph.is_directed() == False else "directed")
print("Is multigraph? - {}".format(graph.is_multigraph()))

a = Infomap(graph)

# print("Number of connected components: {}".format(a.getNumberOfConnectedComponents(graph)))
# print("Number of weakly connected components: {}".format(a.getNumberOfWeaklyConnectedComponents(graph)) if graph.is_directed() else "Weakly connected components not implemented for undirected case")
# print("Number of Isolates: {}".format(a.getNumberOfIsolates(graph)))
# print("Degree Centrality: {}".format(a.getDegreeCentrality(graph)))
# print("Betweeness Centrality: {}".format(a.getBetweenessCentrality(graph)))
# print(a.getNeighbours(graph,1))
# for component in a.getConnectedComponents(graph):
#     subgraph = Graph()
#     for neighbours in component:
#     print("Diameter of {} is: {}\n".format(component,"pass"))
print("Closeness centrality: {}".format(a.getClosenessCentrality(graph)))
print("Katz centrality: {}".format(a.getKatzCentrality(graph)))
print("Pagerank: {}".format(a.getPageRank(graph)))
print("Triangles: {}".format(a.getTriangles(graph)))
print("All Pairs Shortest Path: {}".format(a.getAllPairsShortestPath(graph)))
print("All Pairs Shortest Connectivity: {}".format(a.getAllPairsNodeConnectivity(graph)))
print("Network bridges: {}".format(a.getBridges(graph)))
print("All Connected Components: {}".format(a.getConnectedComponents(graph)))