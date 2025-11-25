class Aresta:
    def __init__(self, u, v, distancia, E_elec=1, E_amp=0.01):
        # Informações básicas
        self._u = u
        self._v = v
        self._distancia = distancia

        # Parâmetros para consumo energético
        self._E_elec = E_elec
        self._E_amp = E_amp

        # Estatísticas
        self._vezes_utilizada = 0
        self._consumo_total = 0.0
    
    def custo_transmissao(self, k=1):
        return self._E_elec * k + self._E_amp * k * (self._distancia ** 2)

    def gastar_energia(self):
        self._vezes_utilizada += 1
        self._consumo_total = self._vezes_utilizada * self._consumo

class Vertice:
    def __init__(self, id, X, Y):
        self._id = id
        self._pos_x = X
        self._pos_y = Y
        self._bateria = 100
    
    def gastar(self, valor):
        self.energia = self._bateria - valor