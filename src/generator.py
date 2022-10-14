import random

TESTE = 10
QTD = 20

def main():
    'Generate a random graph'
    rotas = []
    for i in range(QTD):
        src = random.randint(1, TESTE)
        dest = random.randint(1, TESTE)
        while src == dest or (src, dest) in rotas:
            dest = random.randint(1, TESTE)
        print(f'{src} {dest} {random.randint(1, TESTE)} {random.randint(0, 1)} {random.randint(0, TESTE)}')
        rotas.append((src, dest))

if __name__ == '__main__':
    main()