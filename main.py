"""
Mini ejemplo de plataforma con pygame.

Ejecución:
  pip install pygame
  python main.py
"""

import pygame


def draw_runner(surface: pygame.Surface, rect: pygame.Rect, color: tuple[int, int, int]) -> None:
    """Dibuja un personaje estilo corredor, inspirado en el icono de referencia."""
    x, y, w, h = rect

    # Cabeza
    head_radius = max(5, int(w * 0.18))
    head_center = (x + int(w * 0.72), y + int(h * 0.18))
    pygame.draw.circle(surface, color, head_center, head_radius)

    # Anchura de extremidades
    limb_width = max(4, int(w * 0.12))

    # Torso inclinado
    shoulder = (x + int(w * 0.50), y + int(h * 0.35))
    hip = (x + int(w * 0.36), y + int(h * 0.62))
    pygame.draw.line(surface, color, shoulder, hip, limb_width)

    # Brazo delantero (arriba-derecha)
    hand_front = (x + int(w * 0.92), y + int(h * 0.42))
    pygame.draw.line(surface, color, shoulder, hand_front, limb_width)

    # Brazo trasero (abajo-izquierda)
    hand_back = (x + int(w * 0.14), y + int(h * 0.54))
    pygame.draw.line(surface, color, shoulder, hand_back, limb_width)

    # Pierna delantera (hacia abajo)
    knee_front = (x + int(w * 0.56), y + int(h * 0.72))
    foot_front = (x + int(w * 0.52), y + int(h * 0.94))
    pygame.draw.line(surface, color, hip, knee_front, limb_width)
    pygame.draw.line(surface, color, knee_front, foot_front, limb_width)

    # Pierna trasera (extendida hacia atrás)
    foot_back = (x + int(w * 0.12), y + int(h * 0.74))
    pygame.draw.line(surface, color, hip, foot_back, limb_width)

    # Juntas redondeadas
    joint_radius = max(3, limb_width // 2)
    for joint in (shoulder, hip, knee_front):
        pygame.draw.circle(surface, color, joint, joint_radius)


def draw_ground_box(surface: pygame.Surface, rect: pygame.Rect) -> None:
    """Dibuja suelo tipo caja: 1/3 verde arriba y 2/3 marrón abajo."""
    top_h = max(1, rect.height // 3)
    top_rect = pygame.Rect(rect.left, rect.top, rect.width, top_h)
    bottom_rect = pygame.Rect(rect.left, rect.top + top_h, rect.width, rect.height - top_h)

    pygame.draw.rect(surface, (86, 161, 74), top_rect, border_top_left_radius=8, border_top_right_radius=8)
    pygame.draw.rect(surface, (126, 84, 50), bottom_rect, border_bottom_left_radius=8, border_bottom_right_radius=8)
    pygame.draw.rect(surface, (30, 25, 20), rect, width=2, border_radius=8)


def main() -> None:
    pygame.init()

    width, height = 800, 450
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mapa de plataformas")
    clock = pygame.time.Clock()

    # Entidades
    player_rect = pygame.Rect(150, 220, 90, 120)
    ground_rects = [
        pygame.Rect(60, 55, 220, 45),   # superior izquierda
        pygame.Rect(370, 110, 220, 40), # superior centro
        pygame.Rect(145, 275, 160, 55), # inferior izquierda
        pygame.Rect(350, 225, 210, 55), # centro inferior
        pygame.Rect(640, 170, 120, 110),# bloque vertical derecho
    ]

    # Física
    vel_x = 0.0
    vel_y = 0.0
    gravity = 0.8
    jump_force = -14.0
    speed = 5.0
    on_ground = False

    running = True
    while running:
        jump_requested = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_UP):
                jump_requested = True

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

        # Colisión vertical con plataformas
        on_ground = False
        if vel_y >= 0:
            for ground_rect in ground_rects:
                touching_ground = (
                    player_rect.bottom >= ground_rect.top
                    and player_rect.bottom - int(vel_y) <= ground_rect.top
                    and player_rect.right > ground_rect.left
                    and player_rect.left < ground_rect.right
                )
                if touching_ground:
                    player_rect.bottom = ground_rect.top
                    vel_y = 0.0
                    on_ground = True
                    break

        # Salto cuando está en suelo (espacio o flecha arriba)
        if jump_requested and on_ground:
            vel_y = jump_force
            on_ground = False

        # Dibujo
        screen.fill((31, 43, 68))
        for ground_rect in ground_rects:
            draw_ground_box(screen, ground_rect)
        draw_runner(screen, player_rect, (28, 24, 28))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
