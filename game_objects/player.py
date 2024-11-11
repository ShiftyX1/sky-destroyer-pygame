from const import *
from .bullet import Bullet
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Create a simple aircraft shape
        self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
        
        # Основное тело самолета
        pygame.draw.polygon(self.image, (30, 144, 255), [  # Более яркий синий
            (0, 20),
            (60, 20),
            (30, 0)
        ])
        
        # Хвост самолета
        pygame.draw.polygon(self.image, (30, 144, 255), [
            (20, 20),
            (40, 20),
            (30, 40)
        ])
        
        # Добавляем белую обводку для лучшей видимости
        pygame.draw.polygon(self.image, WHITE, [
            (0, 20),
            (60, 20),
            (30, 0)
        ], 2)
        pygame.draw.polygon(self.image, WHITE, [
            (20, 20),
            (40, 20),
            (30, 40)
        ], 2)
        
        self.rect = self.image.get_rect()
        self.base_x = VIEWPORT_WIDTH // 2  # Базовая позиция по X
        self.rect.centerx = self.base_x
        self.rect.bottom = WORLD_HEIGHT - 100
        self.speed = 5
        self.z_speed = 5
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.gun_offset = 15  # Расстояние от центра до точек стрельбы

    def update(self):
        keys = pygame.key.get_pressed()
        
        # Вертикальное движение
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.z_speed
        if keys[pygame.K_DOWN] and self.rect.bottom < WORLD_HEIGHT:
            self.rect.y += self.z_speed
        
        # Держим игрока в центре по X
        self.rect.centerx = self.base_x

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return [
                # Стреляем из двух точек по бокам от центра самолета
                Bullet(self.rect.centerx - self.gun_offset, self.rect.centery),
                Bullet(self.rect.centerx + self.gun_offset, self.rect.centery)
            ]
        return None