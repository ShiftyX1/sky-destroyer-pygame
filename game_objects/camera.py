import pygame
from const import *

class Camera:
    def __init__(self):
        self.y_offset = WORLD_HEIGHT - VIEWPORT_HEIGHT
        self.x_offset = 0
        self.rotation_speed = 3
        self.max_rotation = VIEWPORT_WIDTH // 2
        
    def apply(self, sprite):
        return pygame.Rect(
            sprite.rect.x - self.x_offset,
            sprite.rect.y - self.y_offset,
            sprite.rect.width,
            sprite.rect.height
        )
    
    def update(self, player):
        desired_y_offset = player.rect.y - VIEWPORT_HEIGHT // 2
        self.y_offset = max(0, min(desired_y_offset, WORLD_HEIGHT - VIEWPORT_HEIGHT))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x_offset = min(self.x_offset + self.rotation_speed, self.max_rotation)
        elif keys[pygame.K_RIGHT]:
            self.x_offset = max(self.x_offset - self.rotation_speed, -self.max_rotation)
        else:
            # Возвращаемся к центру, когда нет нажатых клавиш
            if self.x_offset > 0:
                self.x_offset = max(0, self.x_offset - self.rotation_speed)
            elif self.x_offset < 0:
                self.x_offset = min(0, self.x_offset + self.rotation_speed)