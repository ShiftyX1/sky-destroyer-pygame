from const.colors import *
from const.game_consts import *
from const.system_consts import *
from game_objects.player import Player
from game_objects.enemy import Enemy
from game_objects.bullet import Bullet
from game_objects.cloud import Cloud
from game_objects.camera import Camera
from utils.sound import SoundManager
from utils.glow import draw_glowing_line, draw_glowing_circle
import pygame

pygame.init()
pygame.mixer.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((VIEWPORT_WIDTH, VIEWPORT_HEIGHT))
        pygame.display.set_caption("Su-24: Arcade")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.camera = Camera()
        
        self.sound_manager = SoundManager()
        self.sound_manager.start_background_music()
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        
        self.player = Player()
        self.all_sprites.add(self.player)
        self.player.rect.bottom = WORLD_HEIGHT - 100
        
        for _ in range(10):
            cloud = Cloud()
            self.all_sprites.add(cloud)
            self.clouds.add(cloud)
        
        for _ in range(8):
            self.spawn_enemy()

    def spawn_enemy(self):
        enemy = Enemy()
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def draw_background(self):
        self.screen.fill(BLACK)
        
        visible_horizon = int(HORIZON_Y - self.camera.y_offset)
        
        vanishing_point_x = VIEWPORT_WIDTH//2 - self.camera.x_offset
        vanishing_point_y = VIEWPORT_HEIGHT
        
        if visible_horizon > 0:
            for y in range(min(max(0, visible_horizon), VIEWPORT_HEIGHT)):
                relative_y = (y + self.camera.y_offset) / HORIZON_Y
                relative_y = max(0, min(1, relative_y))
                color_value = int(255 * relative_y)
                color = (135, 206, 235 - color_value//3)
                pygame.draw.line(self.screen, color, (0, y), (VIEWPORT_WIDTH, y))
        
        if visible_horizon < VIEWPORT_HEIGHT:
            water_start = max(0, visible_horizon)
            water_rect = pygame.Rect(0, water_start, VIEWPORT_WIDTH, VIEWPORT_HEIGHT - water_start)
            pygame.draw.rect(self.screen, WATER_BLUE, water_rect)
            
            if visible_horizon > -VIEWPORT_HEIGHT:
                for i in range(10):
                    start_x = VIEWPORT_WIDTH * i // 10
                    start_x_offset = start_x + (self.camera.x_offset * 0.5)
                    pygame.draw.line(self.screen, HORIZON_BLUE,
                                   (start_x_offset, max(0, visible_horizon)),
                                   (vanishing_point_x, vanishing_point_y),
                                   1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets = self.player.shoot()
                    if bullets:
                        self.sound_manager.play_sound('shoot')
                        for bullet in bullets:
                            self.all_sprites.add(bullet)
                            self.bullets.add(bullet)
                elif event.key == pygame.K_m:
                    if self.sound_manager.music_playing:
                        self.sound_manager.stop_background_music()
                    else:
                        self.sound_manager.start_background_music()

    def update(self):
        keys = pygame.key.get_pressed()
        
        for sprite in self.all_sprites:
            if sprite != self.player:
                if keys[pygame.K_LEFT]:
                    sprite.rect.x += self.player.speed
                elif keys[pygame.K_RIGHT]:
                    sprite.rect.x -= self.player.speed
        
        self.all_sprites.update()
        self.camera.update(self.player)
        
        for bullet in self.bullets:
            for enemy in self.enemies:
                if pygame.sprite.collide_rect(bullet, enemy):
                    if abs(bullet.z - enemy.z) < 100:
                        enemy.kill()
                        bullet.kill()
                        self.sound_manager.play_sound('explosion')
                        self.score += int(1000 / enemy.z)
                        self.spawn_enemy()
        
        for enemy in self.enemies:
            if pygame.sprite.collide_rect(self.player, enemy):
                if enemy.z < 150:
                    self.sound_manager.play_sound('explosion')
                    self.running = False

    def draw(self):
        self.draw_background()
        
        for sprite in self.all_sprites:
            screen_position = self.camera.apply(sprite)
            if (screen_position.bottom >= 0 and 
                screen_position.top <= VIEWPORT_HEIGHT):
                self.screen.blit(sprite.image, screen_position)
        
        center_x = VIEWPORT_WIDTH // 2
        center_y = VIEWPORT_HEIGHT // 2
        radius = 30
        pygame.draw.circle(self.screen, (0, 255, 0), (center_x, center_y), radius, 1)
        pygame.draw.line(self.screen, (0, 255, 0), (center_x - 15, center_y), (center_x + 15, center_y), 1)
        pygame.draw.line(self.screen, (0, 255, 0), (center_x, center_y - 15), (center_x, center_y + 15), 1)
        
        font = pygame.font.Font(None, 36)
        
        time_played = pygame.time.get_ticks() // 1000
        minutes = time_played // 60
        seconds = time_played % 60
        time_text = font.render(f'TIME {minutes:02d}:{seconds:02d}', True, (0, 255, 0))
        self.screen.blit(time_text, (10, 10))
        
        score_text = font.render(f'SCORE {str(self.score).zfill(6)}', True, (0, 255, 0))
        self.screen.blit(score_text, (10, 50))
        
        height = WORLD_HEIGHT - self.player.rect.y
        speed = abs(self.camera.x_offset) * 2
        
        speed_text = font.render(f'SPEED', True, (0, 255, 0))
        speed_value = font.render(f'{speed:04d}', True, (0, 255, 0))
        self.screen.blit(speed_text, (20, VIEWPORT_HEIGHT//2 - 40))
        self.screen.blit(speed_value, (20, VIEWPORT_HEIGHT//2))
        
        alt_text = font.render(f'ALT', True, (0, 255, 0))
        alt_value = font.render(f'{height:04d}', True, (0, 255, 0))
        self.screen.blit(alt_text, (VIEWPORT_WIDTH - 100, VIEWPORT_HEIGHT//2 - 40))
        self.screen.blit(alt_value, (VIEWPORT_WIDTH - 100, VIEWPORT_HEIGHT//2))
        
        radar_size = 100
        radar_center = (radar_size + 20, VIEWPORT_HEIGHT - radar_size - 20)
        pygame.draw.circle(self.screen, (0, 255, 0), radar_center, radar_size, 1)
        pygame.draw.line(self.screen, (0, 255, 0), 
                        (radar_center[0] - radar_size, radar_center[1]),
                        (radar_center[0] + radar_size, radar_center[1]), 1)
        pygame.draw.line(self.screen, (0, 255, 0),
                        (radar_center[0], radar_center[1] - radar_size),
                        (radar_center[0], radar_center[1] + radar_size), 1)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

        self.sound_manager.stop_background_music()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
