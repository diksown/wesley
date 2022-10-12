# Esse programa recebe o mapa de uma cidade e faz o cálculo de uma rota no waze.
# n, m
# x1, y1, x2, y2
# As proximas n linhas devem conter m inteiros, 
# onde 0 denota um caminho livre e 1 denota um 
# caminho ocupado (construções, etc)

from math import sqrt
import random
import sys
from time import sleep
from queue import PriorityQueue

def mostra_mapa(mapa, visitado):
    para_mostrar = ""
    for i in range(len(mapa)):
        for j in range(len(mapa[0])):
            if visitado[i][j]:
                para_mostrar += '▒'
            elif mapa[i][j] == 0:
                para_mostrar += ' '
            else:
                para_mostrar += '█'
        para_mostrar += '\n'

    print(para_mostrar)
    print('\n')
    sleep(0.01)

def heuristica(x1, y1, x2, y2):
    return random.random()

def a_star(mapa, x1, y1, x2, y2):
    visitado = [[False for i in range(len(mapa[0]))] for j in range(len(mapa))]
    fila = PriorityQueue()
    fila.put((0, (x1, y1)))
    visitado[x1][y1] = True
    while fila:
        mostra_mapa(mapa, visitado)
        custo, (x, y) = fila.get()
        if x == x2 and y == y2:
            return True
        if x + 1 < len(mapa) and mapa[x + 1][y] == 0 and not visitado[x + 1][y]:
            fila.put((custo + 1 + heuristica(x + 1, y, x2, y2), (x + 1, y)))
            visitado[x + 1][y] = True
        if x - 1 >= 0 and mapa[x - 1][y] == 0 and not visitado[x - 1][y]:
            fila.put((custo + 1 + heuristica(x - 1, y, x2, y2), (x - 1, y)))
            visitado[x - 1][y] = True
        if y + 1 < len(mapa[0]) and mapa[x][y + 1] == 0 and not visitado[x][y + 1]:
            fila.put((custo + 1 + heuristica(x, y + 1, x2, y2), (x, y + 1)))
            visitado[x][y + 1] = True
        if y - 1 >= 0 and mapa[x][y - 1] == 0 and not visitado[x][y - 1]:
            fila.put((custo + 1 + heuristica(x, y - 1, x2, y2), (x, y - 1)))
            visitado[x][y - 1] = True


def dfs(mapa, x1, y1, x2, y2):
    visitado = [[False for i in range(len(mapa[0]))] for j in range(len(mapa))]
    pilha = []
    pilha.append((x1, y1))
    visitado[x1][y1] = True
    while pilha:
        mostra_mapa(mapa, visitado)
        x, y = pilha.pop()
        if x == x2 and y == y2:
            return True
        if x + 1 < len(mapa) and mapa[x + 1][y] == 0 and not visitado[x + 1][y]:
            pilha.append((x + 1, y))
            visitado[x + 1][y] = True
        if x - 1 >= 0 and mapa[x - 1][y] == 0 and not visitado[x - 1][y]:
            pilha.append((x - 1, y))
            visitado[x - 1][y] = True
        if y + 1 < len(mapa[0]) and mapa[x][y + 1] == 0 and not visitado[x][y + 1]:
            pilha.append((x, y + 1))
            visitado[x][y + 1] = True
        if y - 1 >= 0 and mapa[x][y - 1] == 0 and not visitado[x][y - 1]:
            pilha.append((x, y - 1))
            visitado[x][y - 1] = True
    return False

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 main.py <algoritmo>")
        print("Algoritmos disponíveis: dfs, a_star")
        return

    with open('input') as f:
        mapa = []
        for line in f:
            mapa.append(list(map(int, list(line.strip()))))

    n = len(mapa)
    m = len(mapa[0])
    x1, y1, x2, y2 = 0, 0, n - 1, m - 1
    tipo = sys.argv[1]

    if tipo == "dfs":
        # DFS
        dfs(mapa, x1, y1, x2, y2)
    elif tipo == "a_star":
        # A*
        a_star(mapa, x1, y1, x2, y2)
    else: 
        print("Algoritmo inválido. Algoritmos disponíveis: dfs, a_star")
        return


if __name__ == "__main__":
    main()