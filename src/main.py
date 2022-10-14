import sys
from graph import *

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <rota>")
        print("Rotas disponíveis: mais_simples, menor_rota, mais_rapida")
        print("Mais simples: menor número de paradas (nós)")
        print("Menor rota: menor distância percorrida")
        print("Mais rápida: menor tempo de viagem")
        return

    op = sys.argv[1]

    graph = Graph()
    graph.drawGraph()

    if op == 'mais_simples': # bfs
        path = graph.getSimplestPath(1, 7)
        print(path)
        graph.drawPath(path)
    elif op == 'menor_rota': # dijkstra
        path = graph.getShortestPath(10, 8)
        print(path)
        graph.drawPath(path)
    elif op == 'mais_rapida': # A*
        path = graph.astar_path(10, 8)
        print(path)
        graph.drawPath(path)
    else:
        print("Rota inválida. Rotas disponíveis: mais_simples, menor_rota, mais_rapida")
        return

if __name__ == "__main__":
    main()