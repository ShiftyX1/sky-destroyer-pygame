from kivy.core.window import Window
import random

from src.entities.base_entity import BaseEntity
from src.constants.game_constants import (
    ENEMY_SIZE,
    ENEMY_SPEED_MIN,
    ENEMY_SPEED_MAX
)
from src.constants.colors import ENEMY_COLOR

class Enemy(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Установка размеров врага
        self.size = ENEMY_SIZE
        
        # Z-координата для эффекта глубины
        self.z = 1000.0
        self.z_speed = random.uniform(2, 5)
        
        # Инициализация начального состояния
        self.reset()
    
    def reset(self):
        """Сброс позиции и состояния врага"""
        # Случайная начальная позиция сверху экрана
        self.z = 1000.0
        self.active = True
        
        # Размер зависит от z-координаты (эффект приближения)
        size_factor = (1000 - self.z) / 1000
        current_size = tuple(int(x * size_factor) for x in ENEMY_SIZE)
        self.size = current_size
        
        # Случайная позиция по X в пределах экрана
        self.center_x = random.uniform(self.width, Window.width - self.width)
        self.y = Window.height + self.height
        
        # Случайная скорость движения
        self.velocity_y = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        self.velocity_x = random.uniform(-2, 2) * abs(self.velocity_y / ENEMY_SPEED_MIN)
    
    def move(self, dt):
        """Движение врага с учетом z-координаты"""
        if not self.active:
            return
            
        # Обновляем z-координату
        self.z -= self.z_speed
        
        # Обновляем размер в зависимости от z
        if self.z > 0:
            size_factor = (1000 - self.z) / 1000
            current_size = tuple(int(x * size_factor) for x in ENEMY_SIZE)
            self.size = current_size
        
        # Движение по X и Y
        super().move(dt)
        
        # Отражение от краев экрана по X
        if self.x <= 0 or self.right >= Window.width:
            self.velocity_x = -self.velocity_x
        
        # Если враг вышел за пределы экрана или слишком близко (z < 100)
        if self.top < 0 or self.z < 100:
            self.reset()
    
    def on_hit(self):
        """Обработка попадания в врага"""
        self.active = False
        # TODO: Добавить эффект взрыва
        self.reset()