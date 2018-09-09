import matplotlib
import infomap
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
#%matplotlib inline
from Graph import Graph

class Infomap():

    def __init__(self, G):
        self.visualize(G)

    def findCommunities(self, G):
        """
        Partition network with the Infomap algorithm.
        Annotates nodes with 'community' id and return number of communities found.
        """
        infomapWrapper = infomap.Infomap("--two-level --silent")
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
        # plt.savefig("karate.png")
        plt.show()

    def visualize(self, G):
        self.findCommunities(G)
        self.drawNetwork(G)

obj = Graph()
graph = obj.createGraph("Data//dummy.txt")

a = Infomap(graph)