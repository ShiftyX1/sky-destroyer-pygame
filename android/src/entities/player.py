from kivy.core.window import Window
from kivy.vector import Vector
from kivy.clock import Clock

from src.entities.base_entity import BaseEntity
from src.constants.game_constants import (
    PLAYER_SIZE, 
    PLAYER_SPEED, 
    SHOOT_DELAY, 
    GAME_WIDTH
)
from src.constants.colors import PLAYER_COLOR

class Player(BaseEntity):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Установка размеров игрока
        self.size = PLAYER_SIZE
        
        # Начальная позиция игрока
        self.center_x = Window.width / 2
        self.center_y = Window.height * 0.2  # 20% от нижней части экрана
        
        # Игровые параметры
        self.speed = PLAYER_SPEED
        self.last_shot_time = 0
        self.shoot_delay = SHOOT_DELAY
        self.gun_offset = 15  # Расстояние между точками стрельбы
        
        # Ограничения движения
        self.min_x = self.width / 2
        self.max_x = Window.width - self.width / 2
        self.min_y = self.height
        self.max_y = Window.height * 0.8  # Не выше 80% экрана
        
        # Фиксируем центральную позицию по X
        self.base_x = Window.width / 2
    
    def on_touch_move(self, touch):
        """Обработка движения игрока при касании экрана"""
        if touch.y <= self.max_y:  # Ограничение по высоте
            # Плавное движение к точке касания
            target_y = touch.y
            
            # Ограничиваем движение в пределах допустимой зоны
            self.center_y = max(self.min_y, min(target_y, self.max_y))
            # Всегда держим игрока по центру по X
            self.center_x = self.base_x
    
    def shoot(self, spawn_bullet_callback):
        """Создание пуль при выстреле"""
        current_time = Clock.get_time()
        
        if current_time - self.last_shot_time >= self.shoot_delay:
            self.last_shot_time = current_time
            
            # Создаем две пули слева и справа от игрока
            spawn_bullet_callback((self.center_x - self.gun_offset, self.top))
            spawn_bullet_callback((self.center_x + self.gun_offset, self.top))
            
            # TODO: Добавить звук выстрела
            return True
        return False
    
    def reset(self):
        """Сброс состояния игрока"""
        self.center_x = self.base_x
        self.center_y = Window.height * 0.2
        self.velocity_x = 0
        self.velocity_y = 0
        self.last_shot_time = 0
        self.active = True

    def on_size(self, *args):
        """Обработчик изменения размера виджета"""
        # Обновляем ограничения при изменении размера
        self.min_x = self.width / 2
        self.max_x = Window.width - self.width / 2
        self.min_y = self.height
        self.max_y = Window.height * 0.8