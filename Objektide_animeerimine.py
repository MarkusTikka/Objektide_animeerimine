import pygame
import random

pygame.init()

# Mängu akna suurus
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("F1 Mäng")

# Värvid
GRAY = (150, 150, 150)  # Tee hallim toon
GREEN = (76, 208, 56)
WHITE = (255, 255, 255)

# Tee ja joonte suurused
ROAD_WIDTH = 300
MARKER_WIDTH = 10
MARKER_HEIGHT = 50
EDGE_WIDTH = 20  # Valged äärejooned

# Rajad
left_lane = 167
center_lane = 250
right_lane = 333
lanes = [left_lane, center_lane, right_lane]

# Tee ja äärte jooned
road = (100, 0, ROAD_WIDTH, HEIGHT)
left_edge_marker = (100 - EDGE_WIDTH, 0, EDGE_WIDTH, HEIGHT)
right_edge_marker = (400, 0, EDGE_WIDTH, HEIGHT)

# Mängija algpositsioon
player_x = center_lane
player_y = 400

# Laadi pildid
game_bg = pygame.image.load("bg_rally.jpg")
red_car = pygame.image.load("f1_red.png")
blue_car = pygame.image.load("f1_blue.png")

# Kohanda autode suurust
auto_suurus = (50, 100)
red_car = pygame.transform.scale(red_car, auto_suurus)
blue_car = pygame.transform.scale(blue_car, auto_suurus)

# Frame settings
clock = pygame.time.Clock()
fps = 60

# Mängu muutujad
running = True
speed = 5
score = 0
lane_marker_move_y = 0


# Auto klass
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]


# Mängija auto
player = Vehicle(red_car, player_x, player_y)

# Vastaste autod
vehicle_group = pygame.sprite.Group()

while running:
    clock.tick(fps)
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, road)
    pygame.draw.rect(screen, WHITE, left_edge_marker)
    pygame.draw.rect(screen, WHITE, right_edge_marker)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and player.rect.centerx > left_lane:
                player.rect.x -= 83  # Liiguta vasakule vastavalt uutele radadele
            if event.key == pygame.K_RIGHT and player.rect.centerx < right_lane:
                player.rect.x += 83  # Liiguta paremale vastavalt uutele radadele

    # Liikuvad jooned
    lane_marker_move_y += speed
    if lane_marker_move_y >= MARKER_HEIGHT * 2:
        lane_marker_move_y = 0
    for y in range(-MARKER_HEIGHT * 2, HEIGHT, MARKER_HEIGHT * 2):
        pygame.draw.rect(screen, WHITE, (left_lane + 41, y + lane_marker_move_y, MARKER_WIDTH, MARKER_HEIGHT))
        pygame.draw.rect(screen, WHITE, (right_lane - 41, y + lane_marker_move_y, MARKER_WIDTH, MARKER_HEIGHT))

    # Lisa vastase auto
    if len(vehicle_group) < 2:
        lane = random.choice(lanes)
        new_vehicle = Vehicle(blue_car, lane, -auto_suurus[1])
        vehicle_group.add(new_vehicle)

    # Liiguta vastase autosid
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= HEIGHT:
            vehicle.kill()
            score += 1
            if score % 5 == 0:
                speed += 1

    # Kontrolli kokkupõrget
    if pygame.sprite.spritecollide(player, vehicle_group, False):
        running = False
        print("Mäng läbi!")

    # Joonista autod
    vehicle_group.draw(screen)
    screen.blit(player.image, player.rect)

    # Näita skoori
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Skoor: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
