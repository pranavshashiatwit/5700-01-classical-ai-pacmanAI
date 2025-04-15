import pygame
from pygame.locals import *
from constants import *
from vector import Vector2
from entity import Entity
from pathfinder import Pathfinder
from sprites import PacmanSprites

class Pacman(Entity):
    def __init__(self, node, nodeGroup=None, pelletGroup=None):
        super().__init__(node)
        self.name = PACMAN
        self.color = YELLOW
        self.alive = True
        self.ai_mode = True
        self.nodeGroup = nodeGroup
        self.pelletGroup = pelletGroup
        self.search_method = None
        self.sprites = PacmanSprites(self)

    def update(self, dt):
        self.sprites.update(dt)
        if self.ai_mode and self.node == self.target:
            pathfinder = self.nodeGroup.pathfinder
            ghost = getattr(self.nodeGroup, 'ghost', None)
            if self.pelletGroup.pelletList:
                pellet = self.pelletGroup.pelletList[0]
                target, path = pathfinder.compute_target_path(self.node, pellet, search_method=self.search_method)
            else:
                target, path = None, []
            if path and len(path) >= 2:
                new_direction = pathfinder.get_next_direction(path, self.node)
                self.direction = new_direction
                self.target = self.getNewTarget(new_direction)
        self.position += self.directions[self.direction] * self.speed * dt
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            if self.ai_mode:
                pathfinder = self.nodeGroup.pathfinder
                if self.pelletGroup.pelletList:
                    pellet = self.pelletGroup.pelletList[0]
                    target, path = pathfinder.compute_target_path(self.node, pellet, search_method=self.search_method)
                else:
                    target, path = None, []
                if path and len(path) >= 2:
                    self.direction = pathfinder.get_next_direction(path, self.node)
                self.target = self.getNewTarget(self.direction)
            else:
                direction = self.getValidKey()
                self.target = self.getNewTarget(direction)
                if self.target is not self.node:
                    self.direction = direction
                else:
                    self.target = self.getNewTarget(self.direction)
                if self.target is self.node:
                    self.direction = STOP
            self.setPosition()
        else:
            if self.oppositeDirection(self.direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def reset(self):
        super().reset()
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites.reset()

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.position - pellet.position
            dSquared = d.magnitudeSquared()
            rSquared = (pellet.radius + self.collideRadius) ** 2
            if dSquared <= rSquared:
                return pellet
        return None
