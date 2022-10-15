def readInput():
    'Reads input from stdin and returns a list of edges'
    
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