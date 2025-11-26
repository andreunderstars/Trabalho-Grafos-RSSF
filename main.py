import math

from grafo import Vertice, Aresta, Grafo
from visualizer import Tela
from collections import defaultdict, deque

def bfs_pais(adj, raiz=0):
    fila = deque([raiz])
    visitado = set([raiz])

    pai = {raiz: None}  # raiz não tem pai

    while fila:
        u = fila.popleft()
        for v, peso in adj[u]:
            if v not in visitado:
                visitado.add(v)
                pai[v] = u  # registra o pai
                fila.append(v)

    return pai

def caminho_ate_central(pai, sensor):
    caminho = []
    atual = sensor
    
    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]
    
    caminho.reverse()  # coloca da central para o sensor
    return caminho

def enviar_sinal_ate_central(G, pai, sensor_id, custo_sensor=0.01):
    atual = sensor_id

    # se o sensor for a central, nada a fazer
    if sensor_id == 0:
        return

    while pai[atual] is not None:
        proximo = pai[atual]

        # consumo do sensor
        # G.vertices[atual].gastar_energia(custo_sensor)

        # consumo da aresta
        aresta = G.get_aresta(atual, proximo)
        aresta.gastar_energia(G)

        # avança para o próximo vértice no caminho
        atual = proximo


if __name__ == "__main__":
    num = 50
    dataset_path = f"data/Rede {num}.txt"
    G = Grafo()
    sensores = []

    # Lê cada linha do arquivo e cria um vértice para cada uma

    with open(dataset_path, 'r') as f:
        linhas = f.readlines()
    
    # Número de sensores
    n =  int(linhas[0])

    # Coordenadas da central
    cx, cy = map(float, linhas[1].replace(",", " ").split())
    central = Vertice(0, cx, cy)
    sensores.append(central)
    G.adicionar_vertice(0, cx, cy)

    # Coordenadas dos sensores
    for i, linha in enumerate(linhas[2:]):
        linha = linha.replace(",", " ")
        x, y = map(float, linha.split())
        sensor = Vertice(i+1, x, y)
        sensores.append(sensor)
        G.adicionar_vertice(i+1, x, y)

    # Calcula a distância entre cada vértice e cria uma aresta se for menor do que 100m
    for sensor_u in sensores:
        for sensor_v in sensores:

            if sensor_u != sensor_v:
                distancia = math.dist(
                    [sensor_u._pos_x, sensor_u._pos_y],
                    [sensor_v._pos_x, sensor_v._pos_y]
                )
                
                if distancia <= 200:
                    aresta = Aresta(sensor_u._id, sensor_v._id, distancia)
                    G.adicionar_aresta(sensor_u._id, sensor_v._id, distancia)
    
    # visualizer = Tela(1000, 800, G)
    # visualizer.run()
    i = 0
    # Simulação (um while infinito)
    while not G.sensor_morto():
        # Gera uma MST a cada 10 iterações
        if i % 10 == 0:
            mst = G.kruskal()

            # Cria uma lista de adjacências a partir da MST
            adj = defaultdict(list)

            for aresta in mst:
                u = aresta._u
                v = aresta._v
                w = aresta.peso_para_mst(G)

                adj[u].append((v, w))
                adj[v].append((u, w))

            # Ordena a lista
            adj_ordenado = {u: sorted(adj[u], key=lambda x: x[0]) for u in sorted(adj)}
            for u in adj:
                adj_ordenado[u].sort(key=lambda x: x[0])  # ordena pelos IDs dos vizinhos

            pais = bfs_pais(adj_ordenado)

        # Simulação
        for j in range(1, num+1):
            enviar_sinal_ate_central(G, pais, j)

        i += 1
    
    for sensor in range(1, num+1):
        G.info_sensor(sensor)
    print("Iterações:", i)
