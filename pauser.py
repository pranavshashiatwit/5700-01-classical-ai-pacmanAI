from dropdown import Dropdown
from constants import TILEWIDTH, TILEHEIGHT

class Pause:
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0
        self.pauseTime = None
        self.func = None
        self.dropdown = Dropdown(
            options=["A*", "GREEDY", "BFS", "DFS"],
            x=10.5 * TILEWIDTH,
            y=0,
            width=8 * TILEWIDTH,
            height=TILEHEIGHT * 2
        )

    def update(self, dt):
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                if self.func is not None:
                    return self.func
        return None

    def render(self, screen):
        self.dropdown.render(screen)

    def setPause(self, playerPaused=False, pauseTime=None, func=None):
        self.timer = 0
        self.pauseTime = pauseTime
        self.func = func
        self.paused = True

    def flip(self):
        self.paused = not self.paused

    def handle_event(self, event):
        self.dropdown.handle_event(event)
