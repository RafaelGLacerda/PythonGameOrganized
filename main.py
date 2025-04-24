import random 
import pygame
import sys

from attributes import distribuir_pontos
from end import end_screen
from playerBoss import Player, Boss, boss_intro

BOSS_SIZE = 60
win = pygame.display.set_mode((800, 600))
player_idle = pygame.image.load("assets/guerreiro.png").convert_alpha()
clock = pygame.time.Clock()

watcher_img = pygame.image.load("assets/boss1.png").convert_alpha()
watcher_img = pygame.transform.scale(watcher_img, (BOSS_SIZE, BOSS_SIZE))

fury_beast_img = pygame.image.load("assets/boss2.png").convert_alpha()
fury_beast_img = pygame.transform.scale(fury_beast_img, (BOSS_SIZE, BOSS_SIZE))

void_reaper_img = pygame.image.load("assets/boss3.png").convert_alpha()
void_reaper_img = pygame.transform.scale(void_reaper_img, (BOSS_SIZE, BOSS_SIZE))

# Fonte e cores
FONT = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
FPS = 60


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

def main():
    while True:
        attrs = distribuir_pontos()
        player = Player(attrs)

        bosses = [
    Boss(0, 0, 40, 1, "Watcher", 5, watcher_img),
    Boss(0, 0, 70, 1.5, "Fury Beast", 10, fury_beast_img),
    Boss(0, 0, 120, 2, "Void Reaper", 15, void_reaper_img)
]

        current_boss = 0

        if current_boss < len(bosses):
            boss_intro(bosses[current_boss])

        game_over = False

        while not game_over:
            clock.tick(FPS)
            keys = pygame.key.get_pressed()
            now = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == key_bindings["dodge"]:
                    player.dodge()

            player.move(keys)
            player.update()

            if current_boss < len(bosses):
                boss = bosses[current_boss]
                boss.move_towards_player(player)
                boss.ranged_attack(player)

                for proj in boss.projectiles[:]:
                    proj.move()
                    if proj.rect.colliderect(player.rect) and not player.dodging:
                        player.hp -= max(0, proj.damage - player.armor)
                        boss.projectiles.remove(proj)

                if boss.alive and player.rect.colliderect(boss.rect):
                    cooldown = int(1500 / player.attack_speed)
                    if keys[key_bindings["attack"]] and now - player.last_attack > cooldown:
                        player.last_attack = now
                        player.attack_visual_timer = now
                        damage = player.strength
                        if random.random() < player.crit:
                            damage *= 2
                        boss.hp -= damage

                if boss.hp <= 0 and boss.alive:
                    boss.alive = False
                    current_boss += 1
                    if current_boss >= len(bosses):
                        end_screen("Você venceu todos os chefes!")
                        game_over = True
                    else:
                        boss_intro(bosses[current_boss])

            if player.hp <= 0:
                end_screen("Você morreu.")
                game_over = True

            WIN.fill(WHITE)
            player.draw(WIN)
            if current_boss < len(bosses):
                bosses[current_boss].draw(WIN)
            pygame.display.update()

        pygame.display.update()