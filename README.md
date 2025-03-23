# simple_escape_SDU_project_OOP
There is a simpliest game, where you have a blue square (you) must keep going from a collision with the red one (enemy). If it cathes you, you may start again or leave


### 🏆 **Introduction**  

---

### **🚀 Begin**
import pygame
import sys
import random
from abc import ABC, abstractmethod

pygame.init()

_Using some libraries:_ 
_pygame_ - _to create and functioning the game_
_sys_ - _to open and close the programm_
_random_ - _to control enemy`s movement_
---
# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 7
ENEMY_SPEED = 3

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

_Make the display and set RGB colors_
---
# Initializing screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Escape")


_Initialize screen and setting the name_
---
# Abstract class
class GameObject(ABC):
    @abstractmethod
    def draw(self):
        pass

_Creating the Abstract class_
---
# Base class
class Entity(GameObject):
    def __init__(self, x, y, color, size):
        self._x = x  # Incapsulation
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

_First creating the following absract class_
_Then we create incapsulated coordinates, that does not change outside the class. It prevets random collisions_
_draw method is drawing our object, in our case rectangle_
---
# Multiple Inheritance to regulate speed
class SpeedControl:
    def __init__(self, speed):
        self.speed = speed
_It creates the class to regulate the speed_
---
# Multilevel Inheritance 
class MovingEntity(Entity, SpeedControl):
    def __init__(self, x, y, color, size, speed):
        Entity.__init__(self, x, y, color, size)
        SpeedControl.__init__(self, speed)
    
    @abstractmethod
    def move(self, *args):
        pass
_Multilevel inheritance help us to regulate speed both the player and enemy and includes the SpeedControl class_
---
# Player
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
_Creating the player class_
_Giving them the move method and attaching them to the keyboards keys_        
---
# Enemy
class Enemy(MovingEntity):
    def __init__(self, x, y, color, size, speed):
        super().__init__(x, y, color, size, speed)
    
    def move(self, player):
        dx = self.speed if self._x < player.x else -self.speed if self._x > player.x else 0
        dy = self.speed if self._y < player.y else -self.speed if self._y > player.y else 0
        self._x += dx
        self._y += dy
_Creating the Enemy class_
_Giving them speed and direction based on player movement_
_Attaching them to enemy_
---
# Decorator for handling errors
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
_Prevevnting some Errors_
_If they would be, system will close the game_
---
# Game process
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
_Creating a player object in the middle of the display_
_Creating an enemy randomly in range of display area_
_When they are running, display fill the white color_
_Keys are accepting the player`s keyboard tapping_
_Then we check the all players movements, including wheter we close the window, our system will crashes_
_Updating the player movement by taking keyboard key and enemys movement updating if our updates_
_Displaying all_
_Updating the window flip()_
_In case preventing crashing the system if our game will be faster_
---
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
_Filling the screen white when our objects collised_
_Creating the legend "You lost!"_
_Creating the buttons "Again" and "Exit"_
_Drawing the buttons_
_Updating the screen flip()_
---
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

_Infinite cycle to play whether the player do not close the window_
_Closing the window if player closed the window_
_Closing the window if player decided to tap on "Exit"_
_Restarting the game if the player decided to tap on "Again"_
_Game().run() restarts the game from run method_
---
I think the understanding was clear🚀

