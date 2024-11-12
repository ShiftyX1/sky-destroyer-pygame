from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import NumericProperty, ObjectProperty
from kivy.core.window import Window

from ..entities.player import Player
from ..entities.enemy import Enemy
from ..entities.bullet import Bullet
from src.constants.game_constants import *
from ..managers.collision_manager import CollisionManager

class GameScreen(Widget):
    score = NumericProperty(0)
    player = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Инициализация игровых объектов
        self.player = Player()
        self.add_widget(self.player)
        
        # Списки для управления объектами
        self.enemies = []
        self.bullets = []
        self.active_bullets = []  # Активные пули для оптимизации проверки столкновений
        
        # Менеджер столкновений
        self.collision_manager = CollisionManager()
        
        # Создаем начальных врагов
        self._spawn_initial_enemies()
        
        # Запускаем игровой цикл
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        
        # Привязываем обработчики касаний
        Window.bind(on_touch_down=self.on_touch_down)
        Window.bind(on_touch_move=self.on_touch_move)
    
    def _spawn_initial_enemies(self):
        """Создание начальных врагов"""
        for _ in range(MAX_ENEMIES):
            enemy = Enemy()
            self.enemies.append(enemy)
            self.add_widget(enemy)
    
    def _handle_collisions(self):
        """Обработка всех столкновений"""
        # Проверяем столкновения только активных пуль с врагами
        for bullet in self.active_bullets[:]:  # Используем копию списка, так как он может изменяться
            if not bullet.active:
                self.active_bullets.remove(bullet)
                continue
                
            for enemy in self.enemies:
                if enemy.active and self.collision_manager.check_collision(bullet, enemy):
                    # Обработка попадания
                    self.score += SCORE_PER_KILL
                    enemy.on_hit()
                    bullet.on_hit()
                    break
        
        # Проверяем столкновения врагов с игроком
        for enemy in self.enemies:
            if enemy.active and self.collision_manager.check_collision(self.player, enemy):
                self.game_over()
                break
    
    def _spawn_bullet(self, pos):
        """Создание новой пули"""
        # Ищем неактивную пулю для переиспользования
        for bullet in self.bullets:
            if not bullet.active:
                bullet.reset(pos)
                if bullet not in self.active_bullets:
                    self.active_bullets.append(bullet)
                return
        
        # Если нет неактивных пуль, создаем новую
        bullet = Bullet(pos=pos)
        self.bullets.append(bullet)
        self.active_bullets.append(bullet)
        self.add_widget(bullet)
    
    def on_touch_down(self, instance, touch):
        """Обработка касания экрана"""
        if touch.y > PLAY_AREA_TOP:  # Стрельба только в верхней части экрана
            self.player.shoot(self._spawn_bullet)
        return super().on_touch_down(instance, touch)
    
    def on_touch_move(self, instance, touch):
        """Обработка перемещения пальца"""
        if touch.y <= PLAY_AREA_TOP:  # Движение только в игровой зоне
            self.player.on_touch_move(touch)
        return super().on_touch_move(instance, touch)
    
    def update(self, dt):
        """Обновление игрового состояния"""
        # Обновляем все активные объекты
        self.player.move(dt)
        
        for enemy in self.enemies:
            if enemy.active:
                enemy.move(dt)
                # Если враг вышел за пределы экрана, перезапускаем его
                if enemy.top < 0:
                    enemy.reset()
        
        for bullet in self.bullets:
            if bullet.active:
                bullet.move(dt)
                # Если пуля вышла за пределы экрана, деактивируем её
                if bullet.y > Window.height:
                    bullet.deactivate()
                    if bullet in self.active_bullets:
                        self.active_bullets.remove(bullet)
        
        # Проверяем столкновения
        self._handle_collisions()
    
    def game_over(self):
        """Обработка окончания игры"""
        # Останавливаем игровой цикл
        Clock.unschedule(self.update)
        
        # Деактивируем все объекты
        for enemy in self.enemies:
            enemy.deactivate()
        for bullet in self.bullets:
            bullet.deactivate()
        
        # TODO: Показать экран окончания игры
        print(f"Game Over! Score: {self.score}")
    
    def reset_game(self):
        """Сброс игры для начала новой"""
        self.score = 0
        self.player.reset()
        
        # Очищаем все активные объекты
        for enemy in self.enemies:
            enemy.reset()
        for bullet in self.bullets:
            bullet.deactivate()
        self.active_bullets.clear()
        
        # Перезапускаем игровой цикл
        Clock.schedule_interval(self.update, 1.0 / 60.0)