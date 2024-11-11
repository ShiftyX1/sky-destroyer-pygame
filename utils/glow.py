import pygame
import math

def create_glow_surface(color, radius):
    """
    Создает поверхность с эффектом свечения заданного цвета и радиуса
    """
    surface = pygame.Surface((radius * 2 + 1, radius * 2 + 1), pygame.SRCALPHA)
    center = radius + 1
    intensity = 100
    
    for i in range(radius + 1):
        alpha = int((1 - i / radius) * intensity)
        glow_color = (*color[:3], alpha)
        pygame.draw.circle(surface, glow_color, (center, center), radius - i)
    
    return surface

def draw_glowing_line(surface, color, start_pos, end_pos, width=1, glow_radius=50):
    """
    Рисует светящуюся линию
    """
    # Рисуем базовую линию
    pygame.draw.line(surface, color, start_pos, end_pos, width)
    
    # Создаем поверхность для свечения
    glow = create_glow_surface(color, glow_radius)
    
    # Рисуем свечение вдоль линии
    length = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
    for i in range(0, length, glow_radius):
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * i / length
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * i / length
        surface.blit(glow, (x - glow_radius, y - glow_radius), special_flags=pygame.BLEND_RGBA_ADD)

def draw_glowing_circle(surface, color, center, radius, width=1, glow_radius=50):
    """
    Рисует светящийся круг
    """
    # Рисуем базовый круг
    pygame.draw.circle(surface, color, center, radius, width)
    
    # Создаем поверхность для свечения
    glow = create_glow_surface(color, glow_radius)
    
    # Рисуем свечение вокруг круга
    steps = 36  # количество точек свечения
    for i in range(steps):
        angle = 2 * math.pi * i / steps
        x = center[0] + math.cos(angle) * radius - glow_radius
        y = center[1] + math.sin(angle) * radius - glow_radius
        surface.blit(glow, (int(x), int(y)), special_flags=pygame.BLEND_RGBA_ADD)