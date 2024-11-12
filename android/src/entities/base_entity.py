from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector

class BaseEntity(Widget):
    """Базовый класс для всех игровых объектов"""
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = True
    
    def move(self, dt):
        """Перемещение объекта с учетом времени"""
        if self.active:
            self.pos = Vector(*self.velocity) * dt + self.pos
    
    def on_collision(self, other):
        """Обработка столкновений"""
        pass
    
    def deactivate(self):
        """Деактивация объекта (для переиспользования)"""
        self.active = False
        self.velocity_x = 0
        self.velocity_y = 0
    
    def activate(self):
        """Активация объекта"""
        self.active = True