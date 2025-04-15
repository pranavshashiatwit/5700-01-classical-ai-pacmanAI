import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from sprites import GhostSprites

class Ghost(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.randomDirection
        self.sprites = GhostSprites(self)