import pygame
import math

pygame.init()

SCREEN_W, SCREEN_H = 800, 600
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Mundo con cámara y fondo multicolor")

# Tamaño del mundo
WORLD_W, WORLD_H = 2000, 2000

clock = pygame.time.Clock()

# Posición REAL del jugador en el mundo
player_x = WORLD_W // 2
player_y = WORLD_H // 2
player_speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_y -= player_speed
    if keys[pygame.K_s]:
        player_y += player_speed
    if keys[pygame.K_a]:
        player_x -= player_speed
    if keys[pygame.K_d]:
        player_x += player_speed

    # --- CÁMARA ---
    camera_x = player_x - SCREEN_W // 2
    camera_y = player_y - SCREEN_H // 2

    camera_x = max(0, min(camera_x, WORLD_W - SCREEN_W))
    camera_y = max(0, min(camera_y, WORLD_H - SCREEN_H))

    # -----------------------------
    #           DIBUJO
    # -----------------------------
    screen.fill((0, 0, 0))

    # TIEMPO para animación
    t = pygame.time.get_ticks() / 1000

    # FONDO MULTICOLOR EN EL MUNDO
    tile_size = 10
    for x in range(0, WORLD_W, tile_size):
        for y in range(0, WORLD_H, tile_size):
            r = int(128 + 127 * math.sin(t * x))
            g = int(128 + 127 * math.sin(t * y))
            b = int(128 + 127 * math.sin(t * (x + y)))

            pygame.draw.rect(
                screen,
                (r, g, b),
                (x - camera_x, y - camera_y, tile_size, tile_size)
            )

    # JUGADOR (siempre centrado)
    pygame.draw.rect(
        screen,
        (255, 255, 255),
        (SCREEN_W // 2 - 25, SCREEN_H // 2 - 25, 50, 50)
    )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
