from kivy.core.window import Window

# Размеры и физика
GAME_WIDTH = Window.width
GAME_HEIGHT = Window.height
PLAYER_SIZE = (60, 40)
ENEMY_SIZE = (30, 30)
BULLET_SIZE = (10, 10)

# Скорости
PLAYER_SPEED = 5
BULLET_SPEED = 400
ENEMY_SPEED_MIN = -150
ENEMY_SPEED_MAX = -100

# Игровая механика
SHOOT_DELAY = 0.25  # секунды
MAX_ENEMIES = 8
SCORE_PER_KILL = 100

# Зоны игры
PLAY_AREA_TOP = GAME_HEIGHT * 0.8  # Верхние 20% экрана для стрельбы