##################################################
# OBS: A cada execução, o posicionamento dos
# nós utiliza uma seed que optamos por deixá-la
# aleatória, portanto, caso a imagem gerada não
# esteja de acordo com o esperado, basta executar
# novamente o programa.
##################################################

import sys
from graph import *

SOURCE = 10 
TARGET = 8

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

    try:
        if op == 'mais_simples': # bfs
            path = graph.getSimplestPath(SOURCE, TARGET)
        elif op == 'menor_rota': # dijkstra
            path = graph.getShortestPath(SOURCE, TARGET)
        elif op == 'mais_rapida': # A*
            path = graph.astar_path(SOURCE, TARGET)
        else:
            print("Rota inválida. Rotas disponíveis: mais_simples, menor_rota, mais_rapida")
            return

        print(path)
        graph.drawPath(path)
        
    except nx.NetworkXNoPath:
        print("Não há caminho entre os nós {} e {} no grafo".format(SOURCE, TARGET))
        
    except nx.NodeNotFound:
        print("Nó {} ou {} não existe no grafo".format(SOURCE, TARGET))

if __name__ == "__main__":
    main()