"""
Mini ejemplo de plataforma con pygame.

Ejecución:
  pip install pygame
  python main.py
"""

import pygame


def main() -> None:
    pygame.init()

    width, height = 800, 450
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Plataforma básica")
    clock = pygame.time.Clock()

    # Entidades
    player_rect = pygame.Rect(100, 200, 40, 60)
    ground_rect = pygame.Rect(0, height - 80, width, 80)

    # Física
    vel_x = 0.0
    vel_y = 0.0
    gravity = 0.8
    jump_force = -14.0
    speed = 5.0
    on_ground = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and on_ground:
                vel_y = jump_force
                on_ground = False

        keys = pygame.key.get_pressed()
        vel_x = 0.0
        if keys[pygame.K_LEFT]:
            vel_x = -speed
        if keys[pygame.K_RIGHT]:
            vel_x = speed

        # Aplicar físicas
        vel_y += gravity
        player_rect.x += int(vel_x)
        player_rect.y += int(vel_y)

        # Mantener dentro de la ventana en X
        player_rect.left = max(player_rect.left, 0)
        player_rect.right = min(player_rect.right, width)

        # Colisión vertical con suelo
        if vel_y >= 0 and player_rect.colliderect(ground_rect):
            player_rect.bottom = ground_rect.top
            vel_y = 0.0
            on_ground = True
        else:
            on_ground = False

        # Dibujo
        screen.fill((230, 240, 255))
        pygame.draw.rect(screen, (130, 85, 40), ground_rect)
        pygame.draw.rect(screen, (45, 105, 230), player_rect)
        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
