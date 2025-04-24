import random 
import pygame
import sys

pygame.init()
from attributes import distribuir_pontos

win = pygame.display.set_mode((800, 600))
player_idle = pygame.image.load("assets/guerreiro.png").convert_alpha()


# Fonte e cores
FONT = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)



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


def key_config_menu():
    actions = list(key_bindings.keys())
    selected = 0

    while True:
        WIN.fill((245, 245, 245))
        pygame.draw.rect(WIN, (230, 230, 230), (80, 50, 640, 500), border_radius=15)

        title = font.render("Configurar Teclas", True, (40, 40, 40))
        subtitle = pygame.font.SysFont(None, 24).render("Use as Setas do teclado, ENTER para alterar, ESC para sair", True, (100, 100, 100))
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        WIN.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 100))

        for i, action in enumerate(actions):
            key_name = pygame.key.name(key_bindings[action])
            color = (0, 120, 255) if i == selected else (60, 60, 60)
            text = font.render(f"{action.upper()}: {key_name}", True, color)
            WIN.blit(text, (150, 150 + i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(actions)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(actions)
                elif event.key == pygame.K_RETURN:
                    waiting = True
                    while waiting:
                        for e in pygame.event.get():
                            if e.type == pygame.KEYDOWN:
                                key_bindings[actions[selected]] = e.key
                                waiting = False


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

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

player_idle = pygame.image.load("assets/guerreiro.png").convert_alpha()
player_idle = pygame.transform.scale(player_idle, (51, 51))
player_roll = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
player_roll.fill((0, 255, 255))

watcher_img = pygame.image.load("assets/boss1.png").convert_alpha()
watcher_img = pygame.transform.scale(watcher_img, (BOSS_SIZE, BOSS_SIZE))

fury_beast_img = pygame.image.load("assets/boss2.png").convert_alpha()
fury_beast_img = pygame.transform.scale(fury_beast_img, (BOSS_SIZE, BOSS_SIZE))

void_reaper_img = pygame.image.load("assets/boss3.png").convert_alpha()
void_reaper_img = pygame.transform.scale(void_reaper_img, (BOSS_SIZE, BOSS_SIZE))

projectile_image = pygame.Surface((10, 10))
projectile_image.fill((100, 0, 100))
player_attack_image = pygame.Surface((10, 40))
player_attack_image.fill((255, 200, 0))
attack_bar = pygame.Surface((200, 5))
attack_bar.fill(YELLOW)