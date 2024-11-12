from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.animation import Animation

from src.entities.base_entity import BaseEntity
from src.constants.game_constants import (
    BULLET_SIZE,
    BULLET_SPEED
)
from src.constants.colors import BULLET_COLOR

class Bullet(BaseEntity):
    # Для эффекта свечения
    opacity = NumericProperty(1.0)
    
    def __init__(self, pos=None, **kwargs):
        super().__init__(**kwargs)
        
        # Установка размеров пули
        self.size = BULLET_SIZE
        
        # Z-координата для определения дальности
        self.z = 0
        
        # Начальная позиция
        if pos:
            self.pos = pos
        
        # Установка скорости
        self.velocity_y = BULLET_SPEED
        
        # Создаем анимацию свечения
        self.glow_animation = (
            Animation(opacity=0.5, duration=0.1) + 
            Animation(opacity=1.0, duration=0.1)
        )
        self.glow_animation.repeat = True
        self.glow_animation.start(self)
    
    def reset(self, pos):
        """
        Переиспользование пули с новой позицией
        """
        self.z = 0
        self.pos = pos
        self.velocity_y = BULLET_SPEED
        self.active = True
        self.opacity = 1.0
        
        # Перезапускаем анимацию свечения
        self.glow_animation.start(self)
    
    def move(self, dt):
        """
        Движение пули с учетом перспективы
        """
        if not self.active:
            return
            
        # Движение вверх
        super().move(dt)
        
        # Увеличиваем z-координату для эффекта глубины
        self.z += self.velocity_y * dt * 0.5
        
        # Уменьшаем размер пули с расстоянием
        scale = max(0.1, 1 - (self.z / 1000))
        current_size = tuple(int(x * scale) for x in BULLET_SIZE)
        self.size = current_size
        
        # Деактивируем пулю, если она вышла за пределы экрана
        # или слишком далеко улетела
        if self.y > Window.height or self.z > 1000:
            self.deactivate()
    
    def deactivate(self):
        """
        Деактивация пули
        """
        super().deactivate()
        self.glow_animation.stop(self)
        self.opacity = 1.0
    
    def on_hit(self):
        """
        Обработка попадания в цель
        """
        self.deactivate()
        # TODO: Добавить эффект попадания (вспышка или частицы)