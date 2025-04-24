import random 
import pygame
import sys

from menu import main_menu


pygame.init()
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

def end_screen(mensagem):
    while True:
        WIN.fill(WHITE)
        
        # Texto de fim (vitória ou derrota)
        text = FONT.render(mensagem, True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        WIN.blit(text, text_rect)

        # Botões
        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Botão Voltar ao Menu
        menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(WIN, GRAY, menu_button)
        menu_text = FONT.render("Voltar ao Menu", True, BLACK)
        WIN.blit(menu_text, menu_text.get_rect(center=menu_button.center))

        # Botão Sair
        exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
        pygame.draw.rect(WIN, GRAY, exit_button)
        exit_text = FONT.render("Sair do Jogo", True, BLACK)
        WIN.blit(exit_text, exit_text.get_rect(center=exit_button.center))

        pygame.display.update()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if menu_button.collidepoint(mouse_pos):
                    main_menu()
                    return
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()





if __name__ == "__main__":
    main_menu()
    main()