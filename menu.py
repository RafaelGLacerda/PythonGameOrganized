import random 
import pygame
import sys

pygame.init()
from config import key_config_menu

win = pygame.display.set_mode((800, 600))
player_idle = pygame.image.load("assets/guerreiro.png").convert_alpha()


# Fonte e cores
FONT = pygame.font.SysFont(None, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
font = pygame.font.SysFont(None, 36)


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

def main_menu():
    selected = 0
    options = ["Jogar", "Opções", "Sair"]
    title_font = pygame.font.SysFont(None, 64)

    while True:
        WIN.fill((30, 30, 30))
        pygame.draw.rect(WIN, (50, 50, 50), (200, 100, 400, 400), border_radius=15)

        title = title_font.render("Soulslike Game", True, (200, 200, 255))
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 130))

        for i, opt in enumerate(options):
            color = (100, 255, 100) if i == selected else (220, 220, 220)
            text = font.render(opt, True, color)
            WIN.blit(text, (WIDTH//2 - text.get_width()//2, 230 + i * 60))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Jogar":
                        return
                    elif options[selected] == "Opções":
                        key_config_menu()
                    elif options[selected] == "Sair":
                        pygame.quit()
                        sys.exit()
