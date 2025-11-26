import pygame

class Tela:
    def __initi__(self, width, height, simulation):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Visualizador de Rede de Sensores")

        self.running = True
        self.simulation = simulation
        self.display_radius = False
        self.display_paths = False
    
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
                if event.key == pygame.K_c:
                    self.simulation.create_new_simulation("data/Rede 50.txt", 100, "minimum_spanning_tree_prim")
                if event.key == pygame.K_SPACE:
                    self.simulation.run_simulation(1)
                if event.key == pygame.K_DELETE:
                    self.simulation.delete_simulation()
                if event.key == pygame.K_r:
                    self.display_radius = not self.display_radius
                if event.key == pygame.K_p:
                    self.display_paths = not self.display_paths

    def update(self):
        pass

    def draw(self):
        self.screen.fill((255, 255, 255)) 
        self.draw_communication_lines()
        self.draw_paths()
        self.draw_sensors()
        pygame.display.flip()

    