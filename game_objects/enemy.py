import pygame
from const import *
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.z = random.randrange(100, 1000)
        size = int(50 * (1000 - self.z) / 1000)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, RED, 
                          [(0, size//2), (size, size//2), (size//2, 0)])
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(VIEWPORT_WIDTH - self.rect.width)
        min_height = int(WORLD_HEIGHT * 0.1)
        max_height = int(WORLD_HEIGHT * 0.7)
        self.rect.y = random.randrange(min_height, max_height)
        
        self.speed_z = random.randrange(2, 5)
        self.speed_x = random.randrange(-2, 3)

    def update(self):
        self.z -= self.speed_z
        if self.z < 100:
            self.reset()
            
        size = int(50 * (1000 - self.z) / 1000)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, RED, [(0, size//2), (size, size//2), (size//2, 0)])
        
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        
        self.rect.x += self.speed_x
        if self.rect.left < 0 or self.rect.right > VIEWPORT_WIDTH:
            self.speed_x *= -1

    def reset(self):
        self.z = 1000
        self.rect.x = random.randrange(VIEWPORT_WIDTH - self.rect.width)
        min_height = int(WORLD_HEIGHT * 0.1)
        max_height = int(WORLD_HEIGHT * 0.7)
        self.rect.y = random.randrange(min_height, max_height)
        self.speed_x = random.randrange(-2, 3)
