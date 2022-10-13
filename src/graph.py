import matplotlib.pyplot as plt
import networkx as nx
from utils import *

class Graph():
    def __init__(self):
        self.G = nx.DiGraph()

        edges = readInput()

        for edge in edges:
            self.G.add_edge(edge[0], edge[1], weight=edge[2], problem=edge[3], impact=edge[4])
        
        self.pos = nx.spring_layout(self.G)

    def drawGraph(self):
        # nodes
        nx.draw_networkx_nodes(self.G, self.pos, node_size=400)

        # edges
        curvedEdges = [edge for edge in self.G.edges() if reversed(edge) in self.G.edges()]
        straightEdges = list(set(self.G.edges()) - set(curvedEdges))
        trafficCurvedEdges = [edge for edge in curvedEdges if self.G.edges[edge]['problem'] == 1]
        trafficStraightEdges = [edge for edge in straightEdges if self.G.edges[edge]['problem'] == 1]

        curvedEdges = list(set(curvedEdges) - set(trafficCurvedEdges))
        straightEdges = list(set(straightEdges) - set(trafficStraightEdges))

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=curvedEdges,
            width=1,
            edge_color="k",
            style="solid",
            arrows=True,
            arrowstyle="-|>",
            arrowsize=10,
            connectionstyle='arc3, rad = 0.25'
        )

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=straightEdges,
            width=1,
            edge_color="k",
            style="solid",
            arrows=True,
            arrowstyle="-|>",
            arrowsize=10
        )

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=trafficCurvedEdges,
            width=1,
            edge_color="k",
            style="dashed",
            arrows=True,
            arrowstyle="-|>",
            arrowsize=10,
            connectionstyle='arc3, rad = 0.25'
        )

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=trafficStraightEdges,
            width=1,
            edge_color="k",
            style="dashed",
            arrows=True,
            arrowstyle="-|>",
            arrowsize=10
        )

        nx.draw_networkx_labels(self.G, self.pos, font_size=12, font_family="sans-serif") # node labels
        edge_labels = nx.get_edge_attributes(self.G, "weight") # edge weight labels
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels, font_color="orange")

        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

        plt.savefig("network.png")

    def drawPath(self, path):
        pathEdges = []
        for i in range(len(path) - 1):
            pathEdges.append((path[i], path[i+1]))

        curvedEdges = [edge for edge in self.G.edges() if reversed(edge) in self.G.edges()]

        curvedPathEdges = [edge for edge in pathEdges if edge in curvedEdges]
        pathEdges = list(set(pathEdges) - set(curvedPathEdges))

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=curvedPathEdges,
            width=1,
            edge_color="r",
            style="solid",
            arrows=True,
            arrowstyle="-|>",
            arrowsize=10,
            connectionstyle='arc3, rad = 0.25'
        )

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=pathEdges,
            width=1,
            edge_color="r",
            style="solid",
            arrows=True,
            arrowstyle="-|>",
            arrowsize=10
        )

        # edge weight labels
        edge_labels = nx.get_edge_attributes(self.G, "weight")
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels, font_color="orange")

        plt.savefig("network-path.png")
    
    def getShortestPath(self, source, target):
        'Return the shortest path from source to target using Dijkstra algorithm'
        return nx.shortest_path(self.G, source, target, weight='weight')

    def getSimplestPath(self, source, target):
        'Return the simplest path from source to target using BFS algorithm'
        return nx.shortest_path(self.G, source, target, weight=None)


    # def getFastestPath(self, source, target):
    #     'Return the fastest path from source to target using A* algorithm'
    #     def heuristic(u, v):
    #         return self.G.get_edge_data(u, v)['weight']
            
    #     return nx.astar_path(self.G,
    #                         source,
    #                         target,
    #                         heuristic=heuristic,
    #                         weight='weight'
    #                         )