import random 
import pygame
import sys

pygame.init()

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

def distribuir_pontos():
    attributes = {
        "Vida": 100,
        "Força": 10,
        "Armadura": 0,
        "Crítico": 0.1,
        "Vel. Ataque": 1.5
    }
    base_values = attributes.copy()
    options = list(attributes.keys())
    selected = 0
    points = 10

    # Cores
    BG_COLOR = (245, 245, 245)
    BOX_COLOR = (230, 230, 230)
    TEXT_COLOR = (30, 30, 30)
    SELECTED_COLOR = (0, 120, 220)
    BASE_COLOR = (50, 50, 50)
    REMAINING_COLOR = (100, 100, 100)

    while True:
        WIN.fill(BG_COLOR)
        pygame.draw.rect(WIN, BOX_COLOR, (100, 50, WIDTH - 200, HEIGHT - 100), border_radius=20)

        # Títulos
        title = font.render("Distribua seus Pontos", True, TEXT_COLOR)
        subtitle = pygame.font.SysFont(None, 24).render(
            "Use as SETAS para navegar | ENTER para confirmar", True, REMAINING_COLOR
        )

        WIN.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))
        WIN.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 110))

        # Atributos
        for i, key in enumerate(options):
            is_selected = i == selected
            color = SELECTED_COLOR if is_selected else BASE_COLOR
            value = attributes[key]
            base = base_values[key]
            display_text = f"{key:<12} | Base: {base} → Atual: {value}"
            attr_text = font.render(display_text, True, color)

            # Centralizado
            WIN.blit(attr_text, (WIDTH // 2 - attr_text.get_width() // 2, 160 + i * 50))

        # Pontos restantes
        points_text = font.render(f"Pontos restantes: {points}", True, REMAINING_COLOR)
        WIN.blit(points_text, (WIDTH // 2 - points_text.get_width() // 2, HEIGHT - 130))

        pygame.display.update()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RIGHT and points > 0:
                    attributes[options[selected]] += 1
                    points -= 1
                elif event.key == pygame.K_LEFT and attributes[options[selected]] > base_values[options[selected]]:
                    attributes[options[selected]] -= 1
                    points += 1
                elif event.key == pygame.K_RETURN and points == 0:
                    return attributes
