from const import *
import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.z = 0  # Начальная Z-позиция (у игрока)
        self.size = 10  # Начальный размер пули
        
        # Создаем изображение пули
        self.original_size = self.size
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (self.size//2, self.size//2), self.size//2)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.speed_z = 15  # Скорость движения вперед (в глубину)
        self.original_y = float(y)  # Сохраняем начальную Y-позицию как float
        
    def update(self):
        # Движение "вперед" (уменьшение видимого размера)
        self.z += self.speed_z
        
        # Обновляем размер пули в зависимости от расстояния
        scale = max(0.1, 1 - (self.z / 1000))
        self.size = int(self.original_size * scale)
        
        if self.size > 0:
            # Обновляем изображение пули
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            pygame.draw.circle(self.image, WHITE, (self.size//2, self.size//2), self.size//2)
            
            # Обновляем позицию, сохраняя центр
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            
            # Смещаем пулю немного вверх для эффекта перспективы
            self.original_y -= self.speed_z * 0.3
            self.rect.centery = int(self.original_y)
        
        # Удаляем пулю, когда она становится слишком маленькой
        if self.size < 2 or self.z > 1000:
            self.kill()