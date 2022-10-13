import matplotlib.pyplot as plt
import networkx as nx
import sys

def readInput():
    'Return a list of edges from the input file, [[node1, node2, weight, charge], ...]'

    edges= []
    with open('input') as f:
        for line in f:
            edges.append(line.rstrip('\n').split(' '))

    for edge in edges:
        edge[0] = int(edge[0])
        edge[1] = int(edge[1])
        edge[2] = float(edge[2])
        edge[3] = float(edge[3])

    return edges

def graphSetup(edges):
    G = nx.DiGraph()
    for edge in edges:
        G.add_edge(edge[0], edge[1], weight=edge[2], charge=edge[3])

    return G

def drawGraph(G, pos):
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=400)

    # edges
    curvedEdges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
    straightEdges = list(set(G.edges()) - set(curvedEdges))

    nx.draw_networkx_edges(
        G,
        pos,
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
        G,
        pos,
        edgelist=straightEdges,
        width=1,
        edge_color="k",
        style="solid",
        arrows=True,
        arrowstyle="-|>",
        arrowsize=10
    )

    nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif") # node labels
    edge_labels = nx.get_edge_attributes(G, "weight") # edge weight labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_color="orange")

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    plt.savefig("network.png")

def drawPath(G, pos, path):
    'Draw the path in the graph'

    pathEdges = []
    for i in range(len(path) - 1):
        pathEdges.append((path[i], path[i+1]))

    curvedEdges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
    straightEdges = list(set(G.edges()) - set(curvedEdges))

    curvedPathEdges = [edge for edge in pathEdges if edge in curvedEdges]
    pathEdges = list(set(pathEdges) - set(curvedPathEdges))

    nx.draw_networkx_edges(
        G,
        pos,
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
        G,
        pos,
        edgelist=pathEdges,
        width=1,
        edge_color="r",
        style="solid",
        arrows=True,
        arrowstyle="-|>",
        arrowsize=10
    )

    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_color="orange")

    plt.savefig("network-path.png")

def getShortestPath(G, source, target):
    'Return the shortest path from source to target using Dijkstra algorithm'
    return nx.shortest_path(G, source, target, weight='weight')

def getSimplestPath(G, source, target):
    'Return the simplest path from source to target using BFS algorithm'
    return nx.shortest_path(G, source, target, weight=None)

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <rota>")
        print("Rotas disponíveis: mais_simples, menor_rota, mais_rapida, mais_segura")
        print("Mais simples: menor número de paradas (nós)")
        print("Menor rota: menor distância percorrida")
        print("Mais rápida: menor tempo de viagem")
        print("Mais segura: evita regiões (nós) com maior índice de criminalidade")
        return

    op = sys.argv[1]
    edges = readInput()
    G = graphSetup(edges)

    pos = nx.spring_layout(G, seed=None)  # positions for all nodes - seed for reproducibility

    drawGraph(G, pos)

    if op == 'mais_simples': # bfs
        path = getSimplestPath(G, 1, 7)
        print(path)
        drawPath(G, pos, path)
    elif op == 'menor_rota': # dijkstra
        path = getShortestPath(G, 1, 7)
        print(path)
        drawPath(G, pos, path)
    elif op == 'mais_rapida':
        # A*
        pass
    elif op == 'mais_segura':
        # A*
        pass
    else:
        print("Rota inválida. Rotas disponíveis: mais_simples, menor_rota, mais_rapida, mais_segura")
        return

if __name__ == "__main__":
    main()