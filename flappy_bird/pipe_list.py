from pipe import Pipe
import config


class PipeList():
    def __init__(self):
        self.l = [Pipe()]

    def update(self):
        for i in range(len(self.l)-1, -1, -1):
            # Remove pip if it is off screen
            if self.l[i].x <= 0 - config.PIPE_WIDTH:
                self.l.pop(i)
            # Add a pipe if one is halfway
            if self.l[i].x <= config.WIDTH / 2 and 
                self.l[i].x >= (config.WIDTH /2) - (config.PIPE_SPEED / 2):
                self.l.append(Pipe())
            self.l[i].update()

    def draw(self, screen):
        for p in self.l:
            p.draw(screen)

    def no_collision(self, bird):
        