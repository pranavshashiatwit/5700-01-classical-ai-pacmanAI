import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghost
from text import TextGroup
from pauser import Pause
from sprites import MazeSprites
from pathfinder import Pathfinder  # persistent pathfinder instance

class GameController(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.level = 0
        self.textgroup = TextGroup()
        self.pause = Pause(True)

    def setBackground(self):
        self.background = pygame.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.mazesprites = MazeSprites("maze1.txt", "maze1_rotation.txt")
        self.background = self.mazesprites.constructBackground(self.background, self.level % 5)
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.setPortalPair((0, 17), (27, 17))
        self.nodes.pathfinder = Pathfinder(self.nodes)

        ghost_start_node = self.nodes.getNodeFromTiles(13, 17)
        self.ghost = Ghost(ghost_start_node)

        # self.ghost = Ghost(self.nodes.getStartTempNode())
        self.nodes.setGhost(self.ghost)

        self.pellets = PelletGroup("maze1.txt")
        self.pacman = Pacman(self.nodes.getStartTempNode(), nodeGroup=self.nodes, pelletGroup=self.pellets)
        self.pacman.search_method = 'astar'
        self.textgroup.showText(READYTXT)

    def update(self):
        dt = self.clock.tick(30) / 1000.0
        if not self.pause.paused:
            # Use the dropdown value (converted to lower-case) to select the search method.
            self.pacman.search_method = self.pause.dropdown.get_selected().lower()
            self.pacman.update(dt)
            self.ghost.update(dt)
            self.checkPelletEvents()
        self.pause.update(dt)
        self.checkEvents()
        self.render()
        self.textgroup.update(dt)
        self.updateAggregatedMetrics()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            # Pass event to dropdown if paused.
            if self.pause.paused:
                self.pause.handle_event(event)
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pause.paused:
                        if self.pause.func is not None:
                            self.pause.func()
                            self.pause.func = None
                        self.pause.flip()
                        self.textgroup.hideText()
                        self.showEntities()
                    else:
                        self.pause.flip()
                        self.hideEntities()

    def render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        self.textgroup.render(self.screen)
        self.pause.dropdown.render(self.screen)
        if self.pause.paused:
            self.pause.render(self.screen)
        pygame.display.update()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.score += pellet.points
            self.textgroup.updateScore(self.score)
            self.pellets.pelletList.remove(pellet)
            if self.pellets.isEmpty():
                self.hideEntities()
                self.pause.setPause(playerPaused=True, func=self.onLevelComplete)

    def showEntities(self):
        self.pacman.visible = True

    def hideEntities(self):
        self.pacman.visible = False

    def nextLevel(self):
        self.level += 1
        self.startGame()
        self.pause.paused = True

    def updateAggregatedMetrics(self):
        metrics = self.nodes.pathfinder.total_metrics
        line_parts = []
        for algo, stats in metrics.items():
            if stats['calls'] > 0:
                part = f"NODES={stats['nodes_expanded']} PATH={stats['path_length']} CALLS={stats['calls']}"
                line_parts.append(part)
        if line_parts:
            metrics_str = " | ".join(line_parts)
            self.textgroup.updateText(METRICSTXT, metrics_str)


    def onLevelComplete(self):
        # self.updateAggregatedMetrics()
        self.nextLevel()

if __name__ == '__main__':
    game = GameController()
    game.startGame()
    while True:
        game.update()
