from kivy.app import App
from kivy.core.window import Window
from src.ui.game_screen import GameScreen

class SkyDestroyerApp(App):
    def build(self):
        # Устанавливаем ориентацию для мобильных устройств
        Window.orientation = 'portrait'
        # Отключаем мультитач для упрощения управления
        Window.maximize()
        
        return GameScreen()

if __name__ == '__main__':
    SkyDestroyerApp().run()