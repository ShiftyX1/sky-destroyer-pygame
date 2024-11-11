import pygame
import random
from const import *

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, WHITE, (0, 0, 30, 30))
        pygame.draw.ellipse(self.image, WHITE, (15, 0, 30, 30))
        pygame.draw.ellipse(self.image, WHITE, (30, 0, 30, 30))
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(VIEWPORT_WIDTH)
        max_cloud_height = int(WORLD_HEIGHT * 0.6)
        self.rect.y = random.randrange(max_cloud_height)
        self.speed = random.randrange(1, 3)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = VIEWPORT_WIDTH
            max_cloud_height = int(WORLD_HEIGHT * 0.6)
            self.rect.y = random.randrange(max_cloud_height)
            self.speed = random.randrange(1, 3)
