from bird import Bird
import config

class BirdList():

    def __init__(self):
        self.alive = [Bird(color=config.BIRD_COLOR) for _ in range(config.BIRD_NR)]
        self.dead = []

    def update(self, pipe_info):
        for b in self.alive:
            b.update(pipe_info)

    def draw(self, screen):
        for b in self.alive + self.dead:
            b.draw(screen)

    def check_alive(self, pipe_list):
        for i in range(len(self.alive)-1, -1, -1):
            b = self.alive[i]
            if pipe_list.check_collision(b) or b.check_off_screen():
                self.dead.append(self.alive[i])
                self.alive.pop(i)
