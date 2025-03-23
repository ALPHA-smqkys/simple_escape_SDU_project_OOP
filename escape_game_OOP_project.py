import pygame
import sys
import random
from abc import ABC, abstractmethod

pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 6
ENEMY_SPEED = 3

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Инициализация экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape")

# Абстрактный класс
class GameObject(ABC):
    @abstractmethod
    def draw(self):
        pass

# Базовый класс сущности
class Entity(GameObject):
    def __init__(self, x, y, color, size):
        self._x = x  # Инкапсуляция
        self._y = y
        self.color = color
        self.size = size
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self._x, self._y, self.size, self.size))

# Класс для управления скоростью (Multiple Inheritance)
class SpeedControl:
    def __init__(self, speed):
        self.speed = speed

# Промежуточный уровень наследования с множественным наследованием
class MovingEntity(Entity, SpeedControl):
    def __init__(self, x, y, color, size, speed):
        Entity.__init__(self, x, y, color, size)
        SpeedControl.__init__(self, speed)
    
    @abstractmethod
    def move(self, *args):
        pass

# Игрок
class Player(MovingEntity):
    def __init__(self, x, y, color, size, speed):
        super().__init__(x, y, color, size, speed)
    
    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        self._x = (self._x + dx) % WIDTH
        self._y = (self._y + dy) % HEIGHT

# Враг
class Enemy(MovingEntity):
    def __init__(self, x, y, color, size, speed):
        super().__init__(x, y, color, size, speed)
    
    def move(self, player):
        dx = self.speed if self._x < player.x else -self.speed if self._x > player.x else 0
        dy = self.speed if self._y < player.y else -self.speed if self._y > player.y else 0
        self._x += dx
        self._y += dy

# Декоратор для обработки ошибок
class ErrorHandler:
    @staticmethod
    def safe_execute(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Ошибка: {e}")
                pygame.quit()
                sys.exit()
        return wrapper

# Игровой процесс
class Game:
    def __init__(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2, BLUE, 30, PLAYER_SPEED)
        self.enemy = Enemy(random.randint(0, WIDTH), random.randint(0, HEIGHT), RED, 30, ENEMY_SPEED)
        self.clock = pygame.time.Clock()

    @ErrorHandler.safe_execute
    def run(self):
        while True:
            screen.fill(WHITE)
            keys = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.player.move(keys)
            self.enemy.move(self.player)
            
            if pygame.Rect(self.player.x, self.player.y, self.player.size, self.player.size).colliderect(
                pygame.Rect(self.enemy.x, self.enemy.y, self.enemy.size, self.enemy.size)):
                self.show_game_over()
                return
            
            self.player.draw()
            self.enemy.draw()
            pygame.display.flip()
            self.clock.tick(30)
    
    def show_game_over(self):
        screen.fill(WHITE)
        font = pygame.font.Font(None, 50)
        text = font.render("You lost!", True, RED)
        screen.blit(text, (WIDTH // 2 - 90, HEIGHT // 4))
        
        button_font = pygame.font.Font(None, 50)
        restart_text = button_font.render("Again", True, BLACK)
        home_text = button_font.render("Exit", True, BLACK)
        
        restart_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2, 160, 50)
        home_rect = pygame.Rect(WIDTH // 2 + 10, HEIGHT // 2, 160, 50)
        
        pygame.draw.rect(screen, BLUE, restart_rect)
        pygame.draw.rect(screen, BLUE, home_rect)
        
        screen.blit(restart_text, (restart_rect.x + 35, restart_rect.y + 10))
        screen.blit(home_text, (home_rect.x + 45, home_rect.y + 10))
        
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        Game().run()
                        return
                    if home_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

Game().run()
