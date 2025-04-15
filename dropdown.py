import pygame
from pygame.locals import *
from constants import WHITE

class Dropdown:
    def __init__(self, options, x, y, width, height, font_file="PressStart2P-Regular.ttf", font_size=20):
        self.options = options
        self.selected_index = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(font_file, font_size)
        self.expanded = False
        self.option_rects = []

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        selected_text = self.font.render(self.options[self.selected_index], True, WHITE)
        screen.blit(selected_text, (self.x + 5, self.y + (self.height - selected_text.get_height()) // 2))
        if self.expanded:
            self.option_rects = []
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.x, self.y + (i+1)*self.height, self.width, self.height)
                self.option_rects.append(option_rect)
                pygame.draw.rect(screen, WHITE, option_rect, 2)
                option_text = self.font.render(option, True, WHITE)
                screen.blit(option_text, (option_rect.x + 5, option_rect.y + (option_rect.height - option_text.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
            elif self.expanded:
                for i, option_rect in enumerate(self.option_rects):
                    if option_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.expanded = False
                        break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.options)

    def get_selected(self):
        return self.options[self.selected_index]