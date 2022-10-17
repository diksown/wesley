import matplotlib.pyplot as plt
import networkx as nx
from utils import *

from queue import PriorityQueue
import random

G = nx.DiGraph()
TRAFFIC_JAM_FACTOR = 5 # Multiplicidade do impacto do trânsito na rota

class Graph():
    def __init__(self):
        edges = readInput()

        for edge in edges:
            G.add_edge(edge[0], edge[1], weight=edge[2], intensity=edge[3])

        seed = random.randint(0, 1000000)
        # seed = 432279
        print(seed)

        self.pos = nx.spring_layout(G, seed=seed)

    def getNodes(self):
        return G.nodes()

    def drawEdgeList(self, edgeList, color, style, curved):
        if (curved):
            nx.draw_networkx_edges(
                G,
                self.pos,
                edgelist=edgeList,
                width=1,
                edge_color=color,
                style=style,
                arrows=True,
                arrowstyle="-|>",
                arrowsize=10,
                connectionstyle='arc3, rad = 0.25'
            )
            return

        nx.draw_networkx_edges(
            G,
            self.pos,
            edgelist=edgeList,
            width=1,
            edge_color=color,
            style=style,
            arrows=True,
            arrowstyle="-|>",
            arrowsize=10
        )

    def drawGraph(self):
        # nodes
        nx.draw_networkx_nodes(G, self.pos, node_size=400)

        # edges
        curvedEdges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
        straightEdges = list(set(G.edges()) - set(curvedEdges))
        trafficCurvedEdges = [edge for edge in curvedEdges if G.edges[edge]['intensity'] != 0]
        trafficStraightEdges = [edge for edge in straightEdges if G.edges[edge]['intensity'] != 0]
        curvedEdges = list(set(curvedEdges) - set(trafficCurvedEdges))
        straightEdges = list(set(straightEdges) - set(trafficStraightEdges))

        self.drawEdgeList(curvedEdges, "k", "solid", True)
        self.drawEdgeList(straightEdges, "k", "solid", False)
        self.drawEdgeList(trafficCurvedEdges, "k", "dashed", True)
        self.drawEdgeList(trafficStraightEdges, "k", "dashed", False)

        nx.draw_networkx_labels(G, self.pos, font_size=12, font_family="sans-serif") # node labels
        edge_labels = nx.get_edge_attributes(G, "weight") # edge weight labels
        nx.draw_networkx_edge_labels(G, self.pos, edge_labels, font_color="orange")

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

        # edges
        curvedEdges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
        curvedPathEdges = [edge for edge in pathEdges if edge in curvedEdges]
        pathEdges = list(set(pathEdges) - set(curvedPathEdges))

        self.drawEdgeList(curvedPathEdges, "r", "solid", True)
        self.drawEdgeList(pathEdges, "r", "solid", False)

        # edge weight labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, self.pos, edge_labels, font_color="orange")

        plt.savefig("network-path.png")
    
    def getShortestPath(self, source, target):
        'Return the shortest path from source to target using Dijkstra algorithm'
        path = nx.shortest_path(G, source, target, weight='weight')
        totalCost = nx.path_weight(G, path, weight='weight')

        print(f"Custo total: {totalCost}")

        return path

    def getSimplestPath(self, source, target):
        'Return the simplest path from source to target using BFS algorithm'
        path = nx.shortest_path(G, source, target, weight=None)
        totalCost = nx.path_weight(G, path, weight='weight')

        print(f"Custo total: {totalCost}")

        return path

    def aStar(self, source, target):
        if source not in G or target not in G:
            msg = f"Either source {source} or target {target} is not in G"
            raise nx.NodeNotFound(msg)

        OPEN = PriorityQueue()
        CLOSED = {}
        
        # (priority, node, cost, parent)
        OPEN.put((0, source, 0, None))

        while not OPEN.empty():
            _, curnode, dist, parent = OPEN.get()

            if curnode == target:
                path = [curnode]
                node = parent
                print(f"Custo total: {CLOSED[curnode][0]}")
                while node is not None:
                    path.append(node)
                    node = CLOSED[node][1]
                path.reverse()
                return path

            CLOSED[curnode] = (dist, parent)

            for neighbor, info in G[curnode].items():
                cost = dist + info['weight']
                heuristic = TRAFFIC_JAM_FACTOR * info['intensity']
                newCost = cost + heuristic

                if any(neighbor == node[1] and newCost < node[2] for node in OPEN.queue):
                    OPEN.queue = [node for node in OPEN.queue if node[1] != neighbor]
                    # OPEN.put((cost, neighbor, cost, curnode))

                if neighbor in CLOSED:
                    if CLOSED[neighbor][0] < newCost:
                        continue
                    else:
                        CLOSED.pop(neighbor)

                if neighbor not in OPEN.queue and neighbor not in CLOSED:
                    OPEN.put((newCost, neighbor, newCost, curnode))
                    CLOSED[neighbor] = (newCost, curnode)

        raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")