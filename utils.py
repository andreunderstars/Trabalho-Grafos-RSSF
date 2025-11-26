from collections import deque

def bfs_pais(adj, raiz=0):
    fila = deque([raiz])
    visitado = set([raiz])
    pai = {raiz: None}

    while fila:
        u = fila.popleft()
        for v, peso in adj[u]:
            if v not in visitado:
                visitado.add(v)
                pai[v] = u
                fila.append(v)

    return pai

def caminho_ate_central(pai, sensor):
    caminho = []
    atual = sensor
    
    while atual is not None:
        caminho.append(atual)
        atual = pai[atual]
    
    caminho.reverse()
    return caminho

def enviar_sinal_ate_central(G, pai, sensor_id, custo_sensor=0.01):
    atual = sensor_id
    if sensor_id == 0:
        return

    while pai[atual] is not None:
        proximo = pai[atual]
        aresta = G.get_aresta(atual, proximo)
        aresta.gastar_energia(G)
        atual = proximo