import random 
import pygame
import sys

from config import key_config_menu

FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PLAYER_SIZE = 50
BOSS_SIZE = 60
ROLL_SPEED = 8
WALK_SPEED = 4
font = pygame.font.SysFont(None, 36)

projectile_image = pygame.Surface((10, 10))
projectile_image.fill((100, 0, 100))
player_roll = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_roll.fill((0, 255, 255))
player_attack_image = pygame.Surface((10, 40))
player_attack_image.fill((255, 200, 0))

pygame.init()
pygame.font.init()  # Inicializa o módulo de fontes
player_idle = pygame.image.load("assets/guerreiro.png").convert_alpha()

win = pygame.display.set_mode((800, 600))
player_idle = pygame.image.load("assets/guerreiro.png").convert_alpha()


# Fonte e cores
FONT = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
clock = pygame.time.Clock()


pygame.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Top-Down Soulslike")

# Teclas configuráveis (padrões)
key_bindings = {
    "up": pygame.K_w,
    "down": pygame.K_s,
    "left": pygame.K_a,
    "right": pygame.K_d,
    "dodge": pygame.K_SPACE,
    "attack": pygame.K_f
}

class Player:
    def __init__(self, attrs):
        self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = WALK_SPEED
        self.hp = attrs["Vida"]
        self.max_hp = attrs["Vida"]
        self.strength = attrs["Força"]
        self.armor = attrs["Armadura"]
        self.crit = attrs["Crítico"]
        self.attack_speed = attrs["Vel. Ataque"]
        self.dodging = False
        self.dodge_timer = 0
        
        self.image = pygame.transform.scale(player_idle, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        self.last_attack = 0
        self.attack_visual_timer = 0

    def move(self, keys):
        dx = dy = 0
        if keys[key_bindings["up"]]: dy -= 1
        if keys[key_bindings["down"]]: dy += 1
        if keys[key_bindings["left"]]: dx -= 1
        if keys[key_bindings["right"]]: dx += 1

        if self.dodging:
            self.rect.x += dx * ROLL_SPEED
            self.rect.y += dy * ROLL_SPEED
        else:
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def dodge(self):
        self.dodging = True
        self.dodge_timer = pygame.time.get_ticks()
        self.image = player_roll

    def update(self):
        if self.dodging and pygame.time.get_ticks() - self.dodge_timer > 300:
            self.dodging = False
            self.image = player_idle

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

        # Animação de ataque (caso esteja atacando)
        if pygame.time.get_ticks() - self.attack_visual_timer < 150:
            win.blit(player_attack_image, (self.rect.centerx - 5, self.rect.top - 40))

        # Barra de vida
        pygame.draw.rect(win, RED, (10, 10, 200, 20))
        pygame.draw.rect(win, GREEN, (10, 10, 200 * (self.hp / self.max_hp), 20))

        # Barra de recarga de ataque
        time_since_attack = pygame.time.get_ticks() - self.last_attack
        cooldown = int(1500 / self.attack_speed)
        if time_since_attack < cooldown:
            pygame.draw.rect(win, YELLOW, (10, 35, 200 * (time_since_attack / cooldown), 5))
        else:
            pygame.draw.rect(win, YELLOW, (10, 35, 200, 5))

class Projectile:
    def __init__(self, x, y, dx, dy, speed, damage):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.dx = dx
        self.dy = dy
        self.speed = speed
        self.damage = damage
        self.image = projectile_image

    def move(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

    def draw(self, win):
        win.blit(self.image, self.rect.topleft)

class Boss:
    def __init__(self, x, y, hp, speed, name, dmg, image):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, BOSS_SIZE, BOSS_SIZE)
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.name = name
        self.damage = dmg
        self.alive = True
        self.image = image
        self.last_attack = 0
        self.projectiles = []

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))


    def move_towards_player(self, player):
        if not self.alive: return
        dx = dy = 0
        if player.rect.x > self.rect.x: dx = 1
        if player.rect.x < self.rect.x: dx = -1
        if player.rect.y > self.rect.y: dy = 1
        if player.rect.y < self.rect.y: dy = -1
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def ranged_attack(self, player):
        now = pygame.time.get_ticks()
        if now - self.last_attack > 1500:
            self.last_attack = now
            num_proj = random.randint(3, 7)
            for _ in range(num_proj):
                dx = player.rect.centerx - self.rect.centerx + random.randint(-50, 50)
                dy = player.rect.centery - self.rect.centery + random.randint(-50, 50)
                dist = max(1, (dx ** 2 + dy ** 2) ** 0.5)
                self.projectiles.append(Projectile(self.rect.centerx, self.rect.centery, dx / dist, dy / dist, 6, self.damage))

    def draw(self, win):
        if self.alive:
            win.blit(self.image, self.rect.topleft)
            pygame.draw.rect(win, RED, (WIDTH - 210, 10, 200, 20))
            pygame.draw.rect(win, GREEN, (WIDTH - 210, 10, 200 * (self.hp / self.max_hp), 20))
            text = font.render(self.name, True, BLACK)
            win.blit(text, (WIDTH - 210, 35))
            for proj in self.projectiles:
                proj.draw(win)

def boss_intro(boss):
    gate_rect = pygame.Rect(WIDTH // 2 - 50, -100, 100, 200)
    boss.rect.topleft = (WIDTH // 2 - BOSS_SIZE // 2, -BOSS_SIZE)
    name_surface = font.render(boss.name, True, RED)

    intro_timer = pygame.time.get_ticks()
    running = True
    while running:
        clock.tick(FPS)
        WIN.fill(BLACK)

        pygame.draw.rect(WIN, (80, 80, 80), gate_rect)

        if boss.rect.y < 150:
            boss.rect.y += 2
        else:
            WIN.blit(name_surface, (WIDTH // 2 - name_surface.get_width() // 2, HEIGHT // 2))
            if pygame.time.get_ticks() - intro_timer > 3500:
                running = False

        WIN.blit(boss.image, boss.rect.topleft)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
game_over = False
game_won = False
