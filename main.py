import pygame
import math
import sys

pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moteur Raycasting Pseudo-3D (Rétro FPS)")
clock = pygame.time.Clock()

# Carte du monde (1 = Mur, 0 = Vide)
map_data = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,1,0,1],
    [1,0,0,0,1,1,0,0,0,1],
    [1,0,1,0,0,0,0,1,0,1],
    [1,0,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]

MAP_WIDTH = len(map_data[0])
MAP_HEIGHT = len(map_data)
TILE_SIZE = 64

# Position et orientation initiales du joueur
player_x = 1.5 * TILE_SIZE
player_y = 1.5 * TILE_SIZE
player_angle = 0.0
FOV = math.pi / 3  # Champ de vision (60 degrés)
NUM_RAYS = 120     # Nombre de rayons lancés (résolution de l'écran 3D)
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 8 * TILE_SIZE

# Polices
font_medium = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 15)

running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Contrôles fluides du joueur (Déplacement et Rotation)
    keys = pygame.key.get_pressed()
    speed = 3.5
    rot_speed = 0.04

    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        player_angle -= rot_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_angle += rot_speed

    sin_a = math.sin(player_angle)
    cos_a = math.cos(player_angle)

    dx, dy = 0, 0
    if keys[pygame.K_UP] or keys[pygame.K_z]:
        dx += cos_a * speed
        dy += sin_a * speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        dx -= cos_a * speed
        dy -= sin_a * speed

    # Collision simple avec les murs
    new_x = player_x + dx
    new_y = player_y + dy
    if map_data[int(new_y / TILE_SIZE)][int(player_x / TILE_SIZE)] == 0:
        player_y = new_y
    if map_data[int(player_y / TILE_SIZE)][int(new_x / TILE_SIZE)] == 0:
        player_x = new_x

    # --- RENDU GRAPHIQUE ---
    screen.fill((25, 30, 40)) # Couleur du plafond

    # Dessin du sol (moitié inférieure de l'écran)
    floor_rect = pygame.Rect(0, HEIGHT // 2, WIDTH, HEIGHT // 2)
    pygame.draw.rect(screen, (40, 45, 60), floor_rect)

    # Lancer des rayons (Raycasting)
    ray_angle = player_angle - FOV / 2
    column_width = WIDTH / NUM_RAYS

    for ray in range(NUM_RAYS):
        # Algorithme de lancer de rayon pas à pas (Ray Marching)
        distance = 0
        hit_wall = False

        sin_ray = math.sin(ray_angle)
        cos_ray = math.cos(ray_angle)

        while not hit_wall and distance < MAX_DEPTH:
            distance += 4
            test_x = int((player_x + cos_ray * distance) / TILE_SIZE)
            test_y = int((player_y + sin_ray * distance) / TILE_SIZE)

            if test_x < 0 or test_x >= MAP_WIDTH or test_y < 0 or test_y >= MAP_HEIGHT:
                hit_wall = True
                distance = MAX_DEPTH
            elif map_data[test_y][test_x] == 1:
                hit_wall = True

        # Correction de l'effet fish-eye (déformation optique)
        correct_dist = distance * math.cos(player_angle - ray_angle)
        if correct_dist < 1:
            correct_dist = 1

        # Hauteur de la colonne du mur à dessiner
        wall_height = min(HEIGHT, int((TILE_SIZE * 300) / correct_dist))

        # Assombrissement du mur selon la distance (Effet de profondeur / Ombre)
        shade = max(30, min(255, int(255 * (1 - correct_dist / MAX_DEPTH))))
        wall_color = (0, shade, int(shade * 0.7))

        # Dessin de la strie verticale sur l'écran
        wall_rect = pygame.Rect(
            int(ray * column_width),
            int((HEIGHT // 2) - (wall_height // 2)),
            int(column_width) + 1,
            wall_height
        )
        pygame.draw.rect(screen, wall_color, wall_rect)

        ray_angle += DELTA_ANGLE

    # --- MINIMAP (Vue du dessus en haut à gauche) ---
    minimap_scale = 8
    for r in range(MAP_HEIGHT):
        for c in range(MAP_WIDTH):
            color = (255, 255, 255) if map_data[r][c] == 1 else (15, 18, 25)
            pygame.draw.rect(screen, color, (15 + c * minimap_scale, 15 + r * minimap_scale, minimap_scale - 1, minimap_scale - 1))

    # Position du joueur sur la minimap
    p_map_x = int(15 + (player_x / TILE_SIZE) * minimap_scale)
    p_map_y = int(15 + (player_y / TILE_SIZE) * minimap_scale)
    pygame.draw.circle(screen, (0, 255, 157), (p_map_x, p_map_y), 3)

    # Titre et Instructions
    title_txt = font_medium.render("MOTEUR RAYCASTING PSEUDO-3D", True, (255, 255, 255))
    screen.blit(title_txt, (WIDTH - title_txt.get_width() - 20, 15))

    controls_txt = font_small.render("ZQSD / Flèches : Avancer/Reculer & Tourner", True, (130, 140, 160))
    screen.blit(controls_txt, (WIDTH - controls_txt.get_width() - 20, 45))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()