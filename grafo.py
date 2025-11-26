class Aresta:
    def __init__(self, u, v, distancia, E_elec=50e-9, E_amp=100e-12, k=4000):
        # Informações básicas
        self._u = u
        self._v = v
        self._distancia = distancia

        # Parâmetros para consumo energético
        self._E_elec = E_elec
        self._E_amp = E_amp
        self._consumo = self._E_elec * k + self._E_amp * k * (self._distancia ** 2)

        # Estatísticas
        self._vezes_utilizada = 0
        self._consumo_total = 0.0
    
    def gastar_energia(self):
        self._vezes_utilizada += 1
        self._consumo_total = self._vezes_utilizada * self._consumo
    
    def peso_para_mst(self):
        return self._distancia + self._consumo_total


class Vertice:
    def __init__(self, id, X, Y, central=False):
        self._id = id
        self._pos_x = X
        self._pos_y = Y
        self._bateria = 100
        self._central = central
    
    def gastar_energia(self, valor):
        self._bateria -= valor

    def get_posicao(self):
        return (self._pos_x, self._pos_y)

class Grafo:
    def __init__(self):
        self.vertices = {}
        self.arestas = {} 

    def adicionar_vertice(self, id, x, y):
        self.vertices[id] = Vertice(id, x, y)

    def adicionar_aresta(self, u, v, distancia):
        key = frozenset({u, v})
        self.arestas[key] = Aresta(u, v, distancia)

    def get_aresta(self, u, v):
        return self.arestas[frozenset({u, v})]

    def peso(self, u, v):
        return self.arestas[frozenset({u, v})].peso_para_mst()
    
    def imprimir(self):
        print("\n=== VÉRTICES ===")
        for vid, v in self.vertices.items():
            print(f"ID: {vid} | pos=({v._pos_x}, {v._pos_y})")

        print("\n=== ARESTAS ===")
        for key, a in self.arestas.items():
            print(f"{a._u} -- {a._v} | dist={a._distancia:.2f} | consumo_total={a._consumo_total}")

    def info_sensor(self, id_sensor):
        """
        Imprime a bateria restante de um sensor específico.
        """
        if id_sensor not in self.vertices:
            print(f"Sensor {id_sensor} não existe no grafo.")
            return
        
        v = self.vertices[id_sensor]
        print(f"Sensor {id_sensor}: bateria = {v._bateria:.2f}")

    def info_aresta(self, u, v):
        """
        Imprime o consumo total e vezes utilizada de uma aresta específica.
        """
        chave = frozenset({u, v})
        if chave not in self.arestas:
            print(f"Aresta ({u}, {v}) não existe no grafo.")
            return
        
        a = self.arestas[chave]
        print(f"Aresta ({u}, {v}): vezes usada = {a._vezes_utilizada}, consumo total = {a._consumo_total:.2f}")

    def sensor_morto(self):
        """
        Retorna True se qualquer sensor (exceto a central ID 0) tiver bateria <= 0.
        """
        for v_id, v in self.vertices.items():
            if v_id != 0 and v._bateria <= 0:
                return True
        return False

    def kruskal(self):
        n = len(self.vertices)
        uf = UnionFind(n)

        # ordena por peso dinâmico
        arestas_ordenadas = sorted(
            self.arestas.values(),
            key=lambda a: a.peso_para_mst()
        )

        mst = []

        for aresta in arestas_ordenadas:
            u = aresta._u
            v = aresta._v

            if uf.union(u, v):
                mst.append(aresta)

            if len(mst) == n - 1:
                break

        return mst

class UnionFind:
    def __init__(self, n):
        self.pai = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.pai[x] != x:
            self.pai[x] = self.find(self.pai[x])  # compressão de caminho
        return self.pai[x]

    def union(self, a, b):
        raizA = self.find(a)
        raizB = self.find(b)

        if raizA == raizB:
            return False

        # união por rank
        if self.rank[raizA] < self.rank[raizB]:
            self.pai[raizA] = raizB
        elif self.rank[raizA] > self.rank[raizB]:
            self.pai[raizB] = raizA
        else:
            self.pai[raizB] = raizA
            self.rank[raizA] += 1

        return True
