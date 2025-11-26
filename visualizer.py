import pygame

from grafo import Grafo, Vertice, Aresta 
class Tela:
    def __init__(self, width, height, grafo: Grafo):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Visualizador de Rede de Sensores")

        self.running = True
        self.grafo = grafo
        self.display_radius = False
        self.display_arestas = False
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.time.Clock().tick(60)  # Limita a 60 FPS
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.display_arestas = not self.display_arestas

    def update(self):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255)) 
        # self.draw_communication_lines()
        self.draw_Arestas()
        self.draw_Vertices()
        pygame.display.flip()

    def draw_Vertices(self):
        if self.grafo is None:
            return
        
        for sensor in self.grafo.vertices:

            if sensor.central:
                cor = (0, 0, 255)  # Azul para a central
            else:
                
                bateria = sensor.bateria

                if bateria >= 80:
                    cor = (0, 255, 0)  # Verde para bateria alta
                elif bateria >= 50:
                    cor = (255, 255, 0)  # Amarelo para bateria média
                elif bateria >= 20:
                    cor = (255, 165, 0)  # Laranja para bateria baixa
                elif bateria > 0:
                    cor = (255, 0, 0)  # Vermelho para bateria crítica
                else:
                    cor = (128, 128, 128)  # Cinza para sensor morto

            x, y = sensor.get_posicao()
            tela_x = int(round(x/1000 * self.screen.get_width()))
            tela_y = int(round(y/1000 * self.screen.get_height()))
            pygame.draw.circle(self.screen, cor, (tela_x, tela_y), 5)  # Desenha o sensor como um círculo
    
    def draw_Arestas(self):
        if self.grafo is None:
            return
        
        for aresta in self.grafo.arestas.values():
            u = self.grafo.vertices[aresta._u]
            v = self.grafo.vertices[aresta._v]

            x1, y1 = u.get_posicao()
            x2, y2 = v.get_posicao()

            tela_x1 = int(round(x1/1000 * self.screen.get_width()))
            tela_y1 = int(round(y1/1000 * self.screen.get_height()))
            tela_x2 = int(round(x2/1000 * self.screen.get_width()))
            tela_y2 = int(round(y2/1000 * self.screen.get_height()))

            pygame.draw.line(self.screen, (0, 0, 0), (tela_x1, tela_y1), (tela_x2, tela_y2), 1)
    
