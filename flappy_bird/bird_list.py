from bird import Bird
import config

class BirdList():

    def __init__(self):
        self.bl = [Bird for _ in range(config.BIRD_NR)]

    def update(self, pipe_info)
        for b in bl:
            b.update(pipe_info)

    def draw(self, screen):
        for b in bl:
            b.draw(screen)

    def check_alive(self):
        for b in bl:
            b.check_alive()
